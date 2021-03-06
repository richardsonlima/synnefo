# Copyright 2012-2014 GRNET S.A. All rights reserved.
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

from django.test import TestCase

from snf_django.utils.testing import assertGreater, assertIn, assertRaises
from astakos.quotaholder_app import models
import astakos.quotaholder_app.callpoint as qh
from astakos.quotaholder_app.exception import (
    NoCommissionError,
    NoQuantityError,
    NoCapacityError,
    NoHoldingError,
)


class QuotaholderTest(TestCase):

    def issue_commission(self, provisions, name="", force=False):
        return qh.issue_commission(clientkey=self.client,
                                   name=name,
                                   force=force,
                                   provisions=provisions)

    def test_010_qh(self):
        holder = 'h0'
        source = 'system'
        resource1 = 'r1'
        resource2 = 'r2'
        limit1 = 10
        limit2 = 20

        qh.set_quota([((holder, source, resource1), limit1),
                      ((holder, source, resource1), limit2)])

        r = qh.get_quota(holders=[holder], sources=[source],
                         resources=[resource1, resource2])
        self.assertEqual(r, {(holder, source, resource1): (limit2, 0, 0)})

        r = qh.get_quota()
        self.assertEqual(r, {(holder, source, resource1): (limit2, 0, 0)})

        # issuing commissions

        qh.set_quota([((holder, source, resource1), limit1),
                      ((holder, source, resource2), limit2)])

        s1 = self.issue_commission([((holder, source, resource1), limit1/2),
                                    ((holder, source, resource2), limit2)],
                                   name="initial")
        assertGreater(s1, 0)

        r = qh.get_commission(self.client, s1)
        provisions = [
            {'holder': holder,
             'source': source,
             'resource': resource1,
             'quantity': limit1/2,
             },
            {'holder': holder,
             'source': source,
             'resource': resource2,
             'quantity': limit2,
             }
        ]
        self.assertEqual(r['serial'], s1)
        ps = r['provisions']
        for p in ps:
            assertIn(p, provisions)

        with assertRaises(NoCommissionError):
            qh.get_commission(self.client, s1+1)

        # commission exceptions

        with assertRaises(NoCapacityError) as cm:
            self.issue_commission([((holder, source, resource1), 1),
                                   ((holder, source, resource2), 1)])

        e = cm.exception
        provision = e.data['provision']
        self.assertEqual(provision['holder'], holder)
        self.assertEqual(provision['source'], source)
        self.assertEqual(provision['resource'], resource2)
        self.assertEqual(provision['quantity'], 1)
        self.assertEqual(e.data['usage'], limit2)
        self.assertEqual(e.data['limit'], limit2)

        with assertRaises(NoQuantityError) as cm:
            self.issue_commission([((holder, source, resource1), -1)])

        e = cm.exception
        provision = e.data['provision']
        self.assertEqual(provision['holder'], holder)
        self.assertEqual(provision['source'], source)
        self.assertEqual(provision['resource'], resource1)
        self.assertEqual(provision['quantity'], -1)
        self.assertEqual(e.data['usage'], 0)
        self.assertEqual(e.data['limit'], 0)

        with assertRaises(NoHoldingError) as cm:
            self.issue_commission([((holder, source, resource1), 1),
                                   (('nonex', source, resource1), 1)])

        e = cm.exception
        provision = e.data['provision']
        self.assertEqual(provision['holder'], 'nonex')
        self.assertEqual(provision['source'], source)
        self.assertEqual(provision['resource'], resource1)
        self.assertEqual(provision['quantity'], 1)

        r = qh.get_quota(holders=[holder])
        quotas = {(holder, source, resource1): (limit1, 0, limit1/2),
                  (holder, source, resource2): (limit2, 0, limit2),
                  }
        self.assertEqual(r, quotas)

        # resolve commission

        r = qh.get_pending_commissions(clientkey=self.client)
        self.assertEqual(len(r), 1)
        serial = r[0]
        r = qh.resolve_pending_commission(self.client, serial)
        self.assertEqual(r, True)
        r = qh.get_pending_commissions(clientkey=self.client)
        self.assertEqual(r, [])
        r = qh.resolve_pending_commission(self.client, serial)
        self.assertEqual(r, False)

        r = qh.get_quota(holders=[holder])
        quotas = {(holder, source, resource1): (limit1, limit1/2, limit1/2),
                  (holder, source, resource2): (limit2, limit2, limit2),
                  }
        self.assertEqual(r, quotas)

        # resolve commissions

        serial = self.issue_commission([((holder, source, resource1), 1),
                                        ((holder, source, resource2), -1)])

        r = qh.get_quota(holders=[holder])
        quotas = {(holder, source, resource1): (limit1, limit1/2, limit1/2+1),
                  (holder, source, resource2): (limit2, limit2-1, limit2),
                  }
        self.assertEqual(r, quotas)

        r = qh.resolve_pending_commission(self.client, serial, accept=False)
        self.assertEqual(r, True)

        serial1 = self.issue_commission([((holder, source, resource1), 1),
                                         ((holder, source, resource2), -1)])

        serial2 = self.issue_commission([((holder, source, resource1), 1),
                                         ((holder, source, resource2), -1)])

        serial3 = self.issue_commission([((holder, source, resource1), 1),
                                         ((holder, source, resource2), -1)])

        r = qh.resolve_pending_commissions(clientkey=self.client,
                                           accept_set=[serial1, serial2, 0],
                                           reject_set=[serial2, serial3])
        self.assertEqual(r, ([serial1], [serial3], [0], [serial2]))

        r = qh.get_pending_commissions(clientkey=self.client)
        self.assertEqual(r, [serial2])

        # forced commission

        r = qh.get_quota(holders=[holder])
        quotas = {
            (holder, source, resource1): (limit1, limit1/2+1, limit1/2+2),
            (holder, source, resource2): (limit2, limit2-2, limit2-1),
        }
        self.assertEqual(r, quotas)

        with assertRaises(NoCapacityError):
            self.issue_commission(
                [((holder, source, resource1), limit1/2+1)])

        serial = self.issue_commission(
            [((holder, source, resource1), limit1/2+1)],
            force=True)

        r = qh.resolve_pending_commission(self.client, serial, accept=True)
        self.assertEqual(r, True)

        r = qh.get_quota(holders=[holder])
        quotas = {
            (holder, source, resource1): (limit1, limit1+2, limit1+3),
            (holder, source, resource2): (limit2, limit2-2, limit2-1),
        }
        self.assertEqual(r, quotas)

        with assertRaises(NoQuantityError):
            self.issue_commission(
                [((holder, source, resource1), -2*limit1)],
                force=True)

        # release off upper limit

        serial = self.issue_commission([((holder, source, resource1), -1)])
        r = qh.resolve_pending_commission(self.client, serial)
        self.assertEqual(r, True)

        r = qh.get_quota(holders=[holder], resources=[resource1])
        quotas = {
            (holder, source, resource1): (limit1, limit1+1, limit1+2),
        }
        self.assertEqual(r, quotas)

    def test_020_empty_provisions(self):
        serial = self.issue_commission([])
        r = qh.resolve_pending_commission(self.client, serial)
        self.assertEqual(r, True)

    def test_030_set(self):
        holder = 'h0'
        source = 'system'
        resource1 = 'r1'
        resource2 = 'r2'
        limit1 = 10
        limit2 = 20

        models.Holding.objects.create(
            holder=holder, source=source, resource=resource1,
            usage_min=1, usage_max=1, limit=2)
        models.Holding.objects.create(
            holder=holder, source=source, resource=resource2,
            usage_min=2, usage_max=2, limit=22)

        qh.set_quota([((holder, source, resource1), limit1),
                      ((holder, source, resource1), limit2)])

        r = qh.get_quota(holders=[holder])
        self.assertEqual(r, {(holder, source, resource1): (limit2, 1, 1),
                             (holder, source, resource2): (22, 2, 2)})
