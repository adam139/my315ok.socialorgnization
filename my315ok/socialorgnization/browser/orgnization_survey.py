#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _

from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder



from Products.CMFCore import permissions
grok.templatedir('templates') 

class SurveyView(grok.View):
    grok.context(IOrgnization_annual_survey)
    grok.template('survey_pending_view')
    grok.name('baseview')
    grok.require('zope2.View')
    
    def render(self):
        "this is view base class,this function should be override by subclass using template or render."
      
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        from Products.CMFCore.permissions import ModifyPortalContent
        return self.pm().checkPermission(ModifyPortalContent,self.context) 

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='my315ok.socialorgnization',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="chengli")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
                
        brains = self.catalog()({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
        
    def workflow_state(self):
        "context workflow status"
        context = self.context
        wf = getToolByName(context, 'portal_workflow')
        review_state = wf.getInfoFor(context, 'review_state')
        return _(review_state)
    
    @memoize         
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath
         
class SurveyDraftView(SurveyView):
    """survey report view based workflow status: 'draft'"""
    grok.template('survey_draft_view')
    grok.name('draftview')
    grok.require('zope2.View')    
    
       
class SurveyPendingSponsorView(SurveyView):
    """survey report view based workflow status: 'pendsponsor'"""
    grok.template('survey_pending_sponsor_view')
    grok.name('sponsorview')
    grok.require('zope2.View') 
    
class SurveyPendingAgentView(SurveyView):
    """survey report view based workflow status: 'pendingagent'"""
    grok.template('survey_pending_agent_view')
    grok.name('agengtview')
    grok.require('zope2.View')             

class SurveyPublishedView(SurveyView):
    """survey report view based workflow status: 'published'"""
    grok.template('survey_published_view')
    grok.name('publishedview')
    grok.require('zope2.View') 



                 