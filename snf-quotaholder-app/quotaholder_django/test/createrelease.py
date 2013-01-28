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

from config import QHTestCase
from config import run_test_case
from config import rand_string
from config import printf
import os

#def create_entity      OK
#def set_entity_key     OK
#def list_entities      OK
#def get_entity         OK 
#def get_limits         LOVERDOS
#def set_limits         LOVERDOS
#def release_entity     OK
#def get_holding
#def set_holding
#def list_resources     
#def get_quota
#def set_quota
#def issue_commission
#def accept_commission
#def reject_commission
#def get_pending_commissions
#def resolve_pending_commissions
#def get_timeline

class Context(object): 
        entityName = rand_string()
        entityKey = "key1" 
        parentName = "pgerakios"
        parentKey = "key1"

class create_release(object):

    def __init__(self, f):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        print "Inside __init__()"
        self.f = f

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print "Inside __call__()"
        self.f(*args)
        print "After self.f(*args)"


class CreateReleaseListAPITest(QHTestCase):

    entityName = rand_string()
    entityKey = "key1" 
    parentName = "pgerakios"
    parentKey = "key1"

    def createEntity(self):
        printf("Creating entity: {0}", self.entityName)
        rejected = self.qh.create_entity(context={},
                                        create_entity=[(self.entityName,
                                                        self.parentName,
                                                        self.entityKey,
                                                        self.parentKey)])
        self.assertEqual(rejected,[])

    def releaseEntity(self):        
        printf("Releasing entity: {0}", self.entityName)
        rejected = self.qh.release_entity(context={},release_entity=[(self.entityName,
                                                                      self.entityKey)])
        self.assertEqual(rejected,[])

    def checkEntityList(self,exists):
        entityList = self.qh.list_entities(context={},entity=self.parentName,key=self.parentKey)
        if(exists):
            self.assertTrue(self.entityName in entityList)
        else:
            self.assertFalse(self.entityName in entityList)

    def setNewEntityKey(self):
         entityKey2 = rand_string()
         rejected = self.qh.set_entity_key(context={},set_entity_key=[(self.entityName,
                                                                       self.entityKey,
                                                                       entityKey2)])
         self.assertEqual(rejected,[])
         self.entityKey = entityKey2
           
    def checkGetEntity(self,exists):
        entityList = self.qh.get_entity(context={},get_entity=[(self.entityName,
                                                                self.entityKey)])
        if(exists):
            self.assertEqual([(self.entityName,self.parentName)],entityList)
        else:
            self.assertEqual(entityList,[])

    def listResources(self,expected):
        resList = self.qh.list_resources(context={},entity=self.entityName,key=self.entityKey)
        self.assertEqual(expected,resList)

    def setQuota(self,r,q,c,i,e,f):
        rejected = self.qh.set_quota(context={},set_quota=[(self.entityName,r,self.entityKey,q,c,i,e,f)])
        self.assertEqual(rejected,[])
        resList = self.qh.get_quota(context={},get_quota=[(self.entityName,r,self.entityKey)])
        (e0,r1,q1,c1,i1,e1,t0,t1,t2,t3,f1),tail = resList[0],resList[1:]
        self.assertEqual(tail,[])
        self.assertEqual((self.entityName,r,q,c,i,e,f),
                         (e0,r1,q1,c1,i1,e1,f1))

        #    def issueCommission(self):
        # self.qh.issue_commission
    def setUp(self):
        self.qh.create_entity(create_entity=[("pgerakios", "system", "key1", "")])
        self.parentName = "pgerakios"
        self.parentKey = "key1"



    #BUG: max empty name <= 72 
    def test_001(self):
        self.createEntity()
        self.releaseEntity()

    # Test create, list and release
    def test_002(self):
        self.checkEntityList(False)
        self.createEntity()
        self.checkEntityList(True)
        self.releaseEntity()
        self.checkEntityList(False)


    # Test create,set key and release
    def test_003(self):
        self.createEntity()
        self.setNewEntityKey()
        self.setNewEntityKey()
        self.releaseEntity()

    # test get_entity
    def test_004(self):
        self.checkGetEntity(False)
        self.createEntity()
        self.checkGetEntity(True)
        self.releaseEntity()
        self.checkGetEntity(False)

    def test_005(self):
        self.createEntity()
        self.setQuota("res1",10,100,10,10,0)
#        self.listResources([])
        self.releaseEntity()

if __name__ == "__main__":
    import sys
    printf("Using {0}", sys.executable)
    run_test_case(CreateReleaseListAPITest)