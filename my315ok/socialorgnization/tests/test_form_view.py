# -*- coding: UTF-8 -*-
from hashlib import sha1 as sha
from my315ok.socialorgnization.testing import MY315OK_PRODUCTS_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.keyring.interfaces import IKeyManager
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import hmac
import json
import unittest


class TestView(unittest.TestCase):

    layer = MY315OK_PRODUCTS_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        self.portal = portal

    def test_form_view(self):

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader(
            'Authorization', 'Basic %s:%s' %
            (TEST_USER_NAME, TEST_USER_PASSWORD,))

        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@datainout-controlpanel'

        browser.open(obj)

        outstr = "form.button.Export"
        self.assertTrue(outstr in browser.contents)
