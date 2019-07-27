# -*- coding: UTF-8 -*-
from Acquisition import aq_inner
from five import grok
from my315ok.socialorgnization import _
from my315ok.socialorgnization.browser.orgnization_survey import SurveyView
from my315ok.socialorgnization.content.page import IPage
from plone.memoize.instance import memoize
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

import datetime
import json


grok.templatedir('templates')


class PageView(SurveyView):
    """page default view"""
    grok.context(IPage)
    grok.template('page_view')
    grok.name('view')
    grok.require('zope2.View')

    def transfer2text(self, obj):
        try:
            res = obj.output
            return res
        except BaseException:
            return obj
