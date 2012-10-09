# Copyright 2012 GRNET S.A. All rights reserved.
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

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from synnefo.db.models import Backend


class Command(BaseCommand):
    args = "<backend ID>"
    help = "Modify a backend"

    option_list = BaseCommand.option_list + (
        make_option('--clustername',
            dest='clustername',
            help="Set backend's clustername"),
        make_option('--port',
            dest='port',
            help="Set backend's port"),
        make_option('--username',
            dest='username',
            help="Set backend'username"),
        make_option('--password',
            dest='password',
            help="Set backend's password"),
        make_option('--drained',
            dest='drained',
            action='store_true',
            default=False,
            help="Set the backend as drained to exclude from allocation "\
                 "operations"),
        make_option('--no-drained',
            dest='drained',
            action='store_false'),
        make_option('--offline',
            dest='offline',
            action='store_true',
            default=False,
            help="Set the backend as offline to not communicate in order "\
                 "to avoid delays"),
        make_option('--no-offline',
            dest='offline',
            action='store_false')
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Please provide a backend ID")

        try:
            backend_id = int(args[0])
            backend = Backend.objects.get(id=backend_id)
        except ValueError:
            raise CommandError("Invalid backend ID")
        except Backend.DoesNotExist:
            raise CommandError("Backend not found in DB")

        # Ensure fields correspondence with options and Backend model
        fields = ('clustername', 'port', 'username', 'password', 'drained',
                  'offline')
        for field in fields:
            value = options.get(field)
            if value is not None:
                backend.__setattr__(field, value)

        backend.save()