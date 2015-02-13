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

from plone.app.customerize import registration
from zope.traversing.interfaces import ITraverser,ITraversable
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zExceptions import NotFound

from my315ok.socialorgnization import _

from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
from dexterity.membrane.content.member import IOrganizationMember
from xtshzz.policy.behaviors.org import IOrg

from Products.CMFCore import permissions
grok.templatedir('templates') 

class SurveyView(grok.View):
    grok.context(IOrgnization_annual_survey)
    grok.template('survey_draft_view')
    grok.name('baseview')
    grok.require('zope2.View')
#    
#    def render(self):
#        "this is view base class,this function should be override by subclass using template or render."
      
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
    
    @memoize    
    def wf(self):
        context = aq_inner(self.context)
        wf = getToolByName(context, "portal_workflow")
        return wf        
            
    @property
    def isEditable(self):
        from Products.CMFCore.permissions import ModifyPortalContent
        return self.pm().checkPermission(ModifyPortalContent,self.context) 
    
    def formatDatetime(self,Datetimeobj):
        "format Datetime obj to:2015年02月08日"
        year = Datetimeobj.strftime('%Y')
        month = Datetimeobj.strftime('%m')
        day = Datetimeobj.strftime('%d')
        return u"%s年%s月%s日" % (year,month,day)
            
    def created(self):
        "get current context created time. format:2015年02月08日"
        created = self.context.created()
        return self.formatDatetime(created)

    def canbeAuditBySponsor(self):
        status = self.workflow_state()
        return (status == 'pendingsponsor') 
    
    def canbeAuditByAgent(self):
        status = self.workflow_state()
        return (status == 'pendingagent') 
    
    def canbeSubmit(self):
        status = self.workflow_state()
        return (status == 'draft')   
        
    def getCurrentMember(self):
        member_data = self.pm().getAuthenticatedMember()
        id = member_data.getUserName()
#        id = "12@qq.com"   # 测试时适应
        query = {"object_provides":IOrganizationMember.__identifier__,'email':id}
        bns = self.catalog()(query)
        if bns:
            member = bns[0]
            return member
        else:
            return None

    def getSponsorOrg(self):
        "获取上级监管单位名称"
        
        sponsor = IOrg(self.getCurrentMember().getObject()).getSponsor()

        return sponsor
        
    def getSponsorAuditDate(self):
        "获取审核日期"
        return self.created()       
        
    def getSponsorOperator(self):
        "获取上级监管单位的经手人，该经手人，在创建监管单位账号时，由事件更新"
               
        sponsor = self.getSponsorOrg()
        if not sponsor:return None
        from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'Title':sponsor}
        bs = self.catalog()(query)

        if bs: return bs[0].getObject().operator
        return None
    
    def getAgentOrg(self):
        "获取民政局,为民政局 单位对象指定id:minzhengju,以此简便获取到民政局对象"
        
        from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'id':"minzhengju"}
        bs = self.catalog()(query)
#        import pdb
#        pdb.set_trace()        
        if bs: return bs[0].Title
        return None
    
    def getAgentAuditDate(self):
        "获取民政局审核日期"
        return self.getSponsorAuditDate()
    
    def getAgentOperator(self):
        "获取民政局经手人"
        from my315ok.socialorgnization.content.governmentdepartment import IOrgnization
        # 获得该政府部门
        query = {"object_provides":IOrgnization.__identifier__,'id':"minzhengju"}
        bs = self.catalog()(query)
        if bs: return bs[0].getObject().operator
        return None
    
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
        
    def creator(self):
        "get survey report's creator"
        creator = self.context.creators[0]
        return creator
    
    def workflow_state(self):
        "context workflow status"
        context = self.context
        review_state = self.wf().getInfoFor(context, 'review_state')
        return review_state
    
    def workflowHistory(self, complete=True):
        """Return workflow history of this context.

        Taken from plone_scripts/getWorkflowHistory.py
        """
        context = aq_inner(self.context)
        # check if the current user has the proper permissions
#        if not (_checkPermission('Request review', context) or
#            _checkPermission('Review portal content', context)):
#            return []

        workflow = self.wf()
        membership = self.pm()

        review_history = []

        try:
            # get total history
            review_history = workflow.getInfoFor(context, 'review_history')

            if not complete:
                # filter out automatic transitions.
                review_history = [r for r in review_history if r['action']]
            else:
                review_history = list(review_history)

            portal_type = context.portal_type
            anon = _(u'label_anonymous_user', default=u'Anonymous User')

            for r in review_history:
                r['type'] = 'workflow'
                r['transition_title'] = workflow.getTitleForTransitionOnType(
                    r['action'], portal_type) or _("Create")
                r['state_title'] = workflow.getTitleForStateOnType(
                    r['review_state'], portal_type)
                actorid = r['actor']
                r['actorid'] = actorid
                if actorid is None:
                    # action performed by an anonymous user
                    r['actor'] = {'username': anon, 'fullname': anon}
                    r['actor_home'] = ''
                else:
                    r['actor'] = membership.getMemberInfo(actorid)
                    if r['actor'] is not None:
                        r['actor_home'] = self.navigation_root_url + '/author/' + actorid
                    else:
                        # member info is not available
                        # the user was probably deleted
                        r['actor_home'] = ''
            review_history.reverse()

        except WorkflowException:
            log('plone.app.layout.viewlets.content: '
                '%s has no associated workflow' % context.absolute_url(),
                severity=logging.DEBUG)

        return review_history
    
    
    @memoize         
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath
    
### load viewlet
    def __getitem__(self,name):
        viewlet = self.setUpViewletByName(name)
        if viewlet is None:
            active_layers = [ str(x) for x in self.request.__provides__.__iro__]
            active_layers = tuple(active_layers)
            raise RuntimeError("Viewlet does not exist by name %s for the active theme "% name)
        viewlet.update()
        return viewlet.render()
    
    def getViewletByName(self,name):
        views = registration.getViews(IBrowserRequest)
        for v in views:
            if v.provided == IViewlet:
                if v.name == name:
#                    if str(v.required[1]) == '<InterfaceClass plone.app.discussion.interfaces.IDiscussionLayer>':
                        return v
        return None
    
    def setUpViewletByName(self,name):
        context = aq_inner(self.context)
        request = self.request
        reg = self.getViewletByName(name)
        if reg == None:
            return None
        factory = reg.factory
        try:
            viewlet = factory(context,request,self,None).__of__(context)
        except TypeError:
            raise RuntimeError("Unable to initialize viewlet %s. Factory method %s call failed."% name)
        return viewlet    
         
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
#    
#    def render(self):
#        pass     
#    
class SurveyPendingAgentView(SurveyView):
    """survey report view based workflow status: 'pendingagent'"""
    grok.template('survey_pending_agent_view')
    grok.name('agentview')
    grok.require('zope2.View')             
#
#    def render(self):
#        pass
#
class SurveyPublishedView(SurveyView):
    """survey report view based workflow status: 'published'"""
    grok.template('survey_published_view')
    grok.name('publishedview')
    grok.require('zope2.View')
#    
#    def render(self):
#        pass 



                 