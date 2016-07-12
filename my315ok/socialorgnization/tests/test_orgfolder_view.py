#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.socialorgnization.testing import MY315OK_PRODUCTS_FUNCTIONAL_TESTING 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest

from plone.namedfile.file import NamedImage
import os
import datetime

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestOrgnazationFolderView(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_FUNCTIONAL_TESTING


    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="orgnizationfolder1",description="demo orgnizationfolder")     
     
   
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='yuhuqu', 
                                                   )
        
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization2',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 
               
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization3',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 
               


                                
        self.portal = portal                
        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        
        import transaction
        transaction.commit()
        
        page = portal.absolute_url() + '/orgnizationfolder1'

        browser.open(page)


        self.assertTrue('<td class="col-md-1">' in browser.contents)
        
                      