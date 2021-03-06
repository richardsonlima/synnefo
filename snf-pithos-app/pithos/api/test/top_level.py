#!/usr/bin/env python
#coding=utf8

# Copyright 2011-2013 GRNET S.A. All rights reserved.
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

from pithos.api.test import PithosAPITest

from synnefo.lib import join_urls

class TopLevel(PithosAPITest):
    def test_not_allowed_method(self):
        url = join_urls(self.pithos_path, '/')
        r = self.head(url)
        self.assertEqual(r.status_code, 405)
        self.assertTrue('Allow' in r)
        self.assertEqual(r['Allow'], 'GET')
        r = self.put(url, data='')
        self.assertEqual(r.status_code, 405)
        self.assertTrue('Allow' in r)
        self.assertEqual(r['Allow'], 'GET')
        r = self.post(url, data='')
        self.assertEqual(r.status_code, 405)
        self.assertTrue('Allow' in r)
        self.assertEqual(r['Allow'], 'GET')
        r = self.delete(url)
        self.assertEqual(r.status_code, 405)
        self.assertTrue('Allow' in r)
        self.assertEqual(r['Allow'], 'GET')


    def test_authenticate(self):
        url = join_urls(self.pithos_path, '/')
        r = self.get(url, token=None)
        self.assertEqual(r.status_code, 400)

        r = self.get(url, token=None, HTTP_X_AUTH_USER=self.user)
        self.assertEqual(r.status_code, 400)

        r = self.get(url, token=None, HTTP_X_AUTH_USER=self.user,
                     HTTP_X_AUTH_KEY='DummyToken')
        self.assertEqual(r.status_code, 204)
        self.assertTrue('X-Auth-Token' in r)
        self.assertTrue(r['X-Auth-Token'], 'DummyToken')
