# Copyright 2011-2014 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of GRNET S.A.
#

from django.core.management.base import CommandError
from snf_django.management.commands import RemoveCommand
from snf_django.lib.api import faults
from synnefo.logic import networks
from synnefo.management import common


class Command(RemoveCommand):
    can_import_settings = True
    args = "<network_id> [<network_id> ...]"
    help = "Remove a network from the Database, and Ganeti"

    @common.convert_api_faults
    def handle(self, *args, **options):
        if not args:
            raise CommandError("Please provide a network ID")

        force = options['force']
        message = "networks" if len(args) > 1 else "network"
        self.confirm_deletion(force, message, args)

        for network_id in args:
            self.stdout.write("\n")
            try:
                network = common.get_resource("network", network_id,
                                              for_update=True)
                self.stdout.write('Removing network: %s\n' %
                                  network.backend_id)

                networks.delete(network)

                self.stdout.write("Successfully submitted Ganeti jobs to"
                                  " remove network %s\n" % network.backend_id)
            except (CommandError, faults.BadRequest) as e:
                self.stdout.write("Error -- %s\n" % e.message)
