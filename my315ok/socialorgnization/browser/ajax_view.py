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

class SurveyWorkflow(grok.View):
    "接受前台ajax 事件，处理工作流基类"
    grok.name('survey_workflow')   
    grok.require('zope2.View')
    grok.context(IOrgnization_annual_survey)
    
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
    
    def render(self):
        """
        workflow process ,this function should be subclass override.
        """
class SurveySubmit(SurveyWorkflow):
    "接受前台ajax 事件，处理工作流"
    grok.name('survey_workflow_submit')
          
    def render(self):
        """
            接受提交审批事件，确定下一审核人，发送审核通知邮件，反馈结果到前台。
            确定审核人过程：
                1 根据当前提交资料的社团账号，查询对应社团组织，找主管单位。
                    如果有主管单位，则提取主管单位对应的审核账号；
                    如果没有主管单位，则直接提交民政局审核，提取民政局对应的审核账号。
                2 给审核账号发送邮件通知，应该包含对当前年检报告的链接。
                3 更新工作流审批历史
                4 发送反馈到前台：
        input:{status:'pengding';comment:'please approve'}
        output:{}
        """

        userobj = self.pm().getAuthenticatedMember()

        email = userobj.getUserName()
        try:
            member = self.catalog()({'object_provides': IOrganizationMember.__identifier__, 
                              "email":email})[0].getObject()
            return member.absolute_url()
        except:
            return ""      
            



        
