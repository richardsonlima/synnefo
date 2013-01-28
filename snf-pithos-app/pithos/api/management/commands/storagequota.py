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

from pithos.api.settings import (BACKEND_QUOTA, BACKEND_VERSIONING)

from pithos.api.util import get_backend

class Command(BaseCommand):
    args = "<user>"
    help = "Get/set a user's quota"

    option_list = BaseCommand.option_list + (
        make_option('--set-quota',
                    dest='quota',
                    metavar='BYTES',
                    help="Set user's quota"),
    )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Please provide a user")

        user = args[0]
        quota = options.get('quota')
        if quota is not None:
            try:
                quota = int(quota)
            except ValueError:
                raise CommandError("Invalid quota")

        backend = get_backend()
        backend.default_policy['quota'] = BACKEND_QUOTA
        backend.default_policy['versioning'] = BACKEND_VERSIONING

        if backend.using_external_quotaholder:
            raise CommandError("The system uses an extrenal quota holder.")

        if quota is not None:
            backend.update_account_policy(user, user, {'quota': quota})
        else:
            self.stdout.write("Quota for %s: %s\n" % (
                user, backend.get_account_policy(user, user)['quota']))
        backend.close()