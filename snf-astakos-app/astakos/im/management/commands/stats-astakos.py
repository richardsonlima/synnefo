# Copyright 2013 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.
from __future__ import division
import json
import string
from optparse import make_option

from snf_django.management.commands import SynnefoCommand, CommandError
from snf_django.management.utils import pprint_table
#from astakos.im.models import AstakosUser, Resource
#from astakos.quotaholder_app.models import Holding
from astakos.admin import stats as statistics
from astakos.im.models import Resource
from synnefo.util import units
from astakos.im.management.commands import _common as common

RESOURCES = Resource.objects.values_list("name", "desc")

HELP_MSG = """Get available statistics of Astakos Service

Display statistics for users and resources for each Authentication
Provider.

Users
------
 * total: Number of users
 * verified: Number of verified users
 * active: Number of activated users


Resources
---------
For each resource the following information is displayed:

 * used: Current allocated resources
 * limit: Maximum allowed allocation

The available resources are the following:

 * {resources}
""".format(resources="\n * ".join(["%s: %s" % (name, desc)
                                   for name, desc in RESOURCES]))


class Command(SynnefoCommand):
    help = HELP_MSG
    can_import_settings = True

    option_list = SynnefoCommand.option_list + (
        make_option('--unit-style',
                    default='auto',
                    help=("Specify display unit for resource values "
                          "(one of %s); defaults to auto") %
                    common.style_options),
    )

    def handle(self, *args, **options):
        stats = statistics.get_astakos_stats()
        unit_style = options["unit_style"]
        common.check_style(unit_style)

        output_format = options["output_format"]
        if output_format == "json":
            self.stdout.write(json.dumps(stats, indent=4) + "\n")
        elif output_format == "pretty":
            pretty_print_stats(stats, unit_style, self.stdout)
        else:
            raise CommandError("Output format '%s' not supported." %
                               output_format)


def columns_from_fields(fields, values):
    return zip(map(string.lower, fields), [values.get(f, 0) for f in fields])


def pretty_print_stats(stats, unit_style, stdout):
    newline = lambda: stdout.write("\n")

    _datetime = stats.get("datetime")
    stdout.write("datetime: %s\n" % _datetime)
    newline()

    user_stats = stats.get("users", {})
    table = []
    headers = ["Provider Name", "Verified Users", "Active Users",
               "Total Users"]
    for provider, user_info in sorted(user_stats.items()):
        table.append((provider, user_info["verified"], user_info["active"],
                      user_info["total"]))
    pprint_table(stdout, table, headers,
                 title="Users")

    newline()
    resource_stats = stats.get("resources", {})
    total_resources = {}
    headers = ["Resource Name", "Used", "Limit", "Usage"]
    for provider, resources in sorted(resource_stats.items()):
        table = []
        for resource_name, resource_info in sorted(resources.items()):
            unit = resource_info["unit"]
            used = resource_info["used"]
            limit = resource_info["limit"]
            usage = round(used / limit, 1)
            table.append((resource_name,
                          units.show(used, unit, style=unit_style),
                          units.show(limit, unit, style=unit_style),
                          usage))
            # Also count them for total
            total_resources.setdefault(resource_name, {})
            total_resources[resource_name].setdefault("used", 0)
            total_resources[resource_name].setdefault("limit", 0)
            total_resources[resource_name]["used"] += used
            total_resources[resource_name]["limit"] += limit
            total_resources[resource_name]["unit"] = unit
        pprint_table(stdout, table, headers,
                     title="Resources for Provider '%s'" % provider)
        newline()

    if len(resource_stats) > 1:
        table = []
        for resource_name, resource_info in sorted(total_resources.items()):
            unit = resource_info["unit"]
            used = resource_info["used"]
            limit = resource_info["limit"]
            usage = round(used / limit, 1)
            table.append((resource_name,
                          units.show(used, unit, style=unit_style),
                          units.show(limit, unit, style=unit_style),
                          usage))
        pprint_table(stdout, table, headers,
                     title="Resources for all Providers")
        newline()
