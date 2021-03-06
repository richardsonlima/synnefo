# -*- coding: utf-8 -
#
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

import ConfigParser


class WorkerGlue(object):

    pmap = {}
    worker_id = None
    ioctx_pool = None
    ArchipelagoConfFile = None

    @classmethod
    def setmap(cls, pid, index):
        WorkerGlue.pmap[pid] = index
        WorkerGlue.worker_id = index

    @classmethod
    def setupXsegPool(cls, ObjectPool, Segment, Xseg_ctx,
                      cfile='/etc/archipelago/archipelago.conf', pool_size=8):
        if WorkerGlue.ioctx_pool is not None:
            return
        bcfg = ConfigParser.ConfigParser()
        bcfg.readfp(open(cfile))
        worker_id = WorkerGlue.worker_id
        WorkerGlue.ArchipelagoConfFile = cfile
        archipelago_segment_type = 'segdev'
        archipelago_segment_name = 'xsegbd'
        archipelago_dynports = bcfg.getint('XSEG', 'SEGMENT_DYNPORTS')
        archipelago_ports = bcfg.getint('XSEG', 'SEGMENT_PORTS')
        archipelago_segment_size = bcfg.getint('XSEG', 'SEGMENT_SIZE')
        archipelago_segment_alignment = 12

        class XsegPool(ObjectPool):

            def __init__(self):
                super(XsegPool, self).__init__(size=pool_size)
                self.segment = Segment(archipelago_segment_type,
                                       archipelago_segment_name,
                                       archipelago_dynports,
                                       archipelago_ports,
                                       archipelago_segment_size,
                                       archipelago_segment_alignment)
                self.worker_id = worker_id
                self.cnt = 1

            def _pool_create(self):
                if self.worker_id == 1:
                    ioctx = Xseg_ctx(self.segment, self.worker_id + self.cnt)
                    self.cnt += 1
                    return ioctx
                elif self.worker_id > 1:
                    ioctx = Xseg_ctx(self.segment,
                                     (self.worker_id - 1) * pool_size + 2 +
                                     self.cnt)
                    self.cnt += 1
                    return ioctx
                elif self.worker_id is None:
                    ioctx = Xseg_ctx(self.segment)
                    return ioctx

            def _pool_verify(self, poolobj):
                return True

            def _pool_cleanup(self, poolobj):
                return False

        WorkerGlue.ioctx_pool = XsegPool()
