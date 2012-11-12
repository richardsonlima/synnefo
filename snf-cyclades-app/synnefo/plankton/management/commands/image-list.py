# Copyright 2011-2012 GRNET S.A. All rights reserved.
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

from django.core.management.base import BaseCommand
from optparse import make_option

from synnefo.plankton.backend import ImageBackend


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--user-id', dest='userid',
            help="List all images available to that user"),
        )

    def handle(self, **options):
        userid = options['userid']
        write = self.stdout.write

        c = ImageBackend(userid) if userid else ImageBackend("")
        images = c.list()
        images.sort(key=lambda x: x['created_at'], reverse=True)

        fields = ("id", "name", "owner", "public")
        columns = (40, 30, 30, 7)
        sep = "-" * 107
        line = "".join(f.rjust(c) for f, c in zip(fields, columns))
        write(line + "\n")
        write(sep + "\n")
        for img in images:
            fields = (img["id"], img["name"], img["owner"], img["is_public"])
            line = "".join(str(f).rjust(c) for f, c in zip(fields, columns))
            write(line + "\n")