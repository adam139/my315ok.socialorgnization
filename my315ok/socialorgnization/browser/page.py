#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from my315ok.socialorgnization.content.page import IPage
from my315ok.socialorgnization.browser.orgnization_survey import SurveyView 
from my315ok.socialorgnization import _


grok.templatedir('templates')

class PageView(SurveyView):
    """page default view"""
    grok.context(IPage)
    grok.template('page_view')
    grok.name('view')
    grok.require('zope2.View')    

    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj