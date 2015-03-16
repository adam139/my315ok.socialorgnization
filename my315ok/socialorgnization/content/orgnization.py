#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
import datetime

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from collective import dexteritytextindexer

#from collective.dexteritytextindexer.behavior import IDexterityTextIndexer
from my315ok.socialorgnization.registrysource import DynamicVocabulary
from my315ok.socialorgnization import _

class IOrgnization(form.Schema,IBasic):
    """
    orgnization content type
    """
#名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"orgnization name"),
                             default=u"",
                            required=True,) 
#经营范围        
    description = schema.TextLine(title=_(u"sector"),
                             default=u"",
                             required=False,)
#   住所 
    address = schema.TextLine(title=_(u"Address"),
                             default=u"",
                             required=False,)
#   法人     
    legal_person = schema.TextLine(title=_(u"legal person"),
                             default=u"",
                             required=True,)
# 主管单位    
    supervisor = schema.TextLine(title=_(u"supervisor organization"),
                             default=u"",
                             required=True,)    
#登记证号    
    register_code = schema.ASCIILine(
            title=_("label_register_code",
                default=u"register code"),
            description=_("help_register_code",
                default=u"A code identifying this organization."),
            required=True)
#组织类别            
    organization_type = schema.Choice(
        title=_(u"organization Type"),
        vocabulary="my315ok.socialorgnization.vocabulary.organizationtype"
    )
    
#归属地区：市本级/湘潭县/韶山           
    belondto_area = schema.Choice(
        title=_(u"belondto area"),
        vocabulary="my315ok.socialorgnization.vocabulary.belondtoarea",
        default ="xiangtanshi"
    ) 
        
#公告类别：成立/变更/注销            
    announcement_type = schema.Choice(
        title=_(u"announcement Type"),
        vocabulary="my315ok.socialorgnization.vocabulary.announcementtype"
    ) 
# 批准日期

    passDate = schema.Date(
        title=_(u"Pass Date"),
        description=u'',
        required=True,
    )
#   公章     
    image = NamedBlobImage(title=_(u"public sign"),
                             description=_(u"a image of the public sign"),
                             required=False,)    

class ICostomTitle(Interface):
    """Get the name from parent object's id.
    This is really just a marker interface.
    """
@grok.provider(IContextSourceBinder)
def possibleOrganization(context):
         

    terms = []
    value = context.title  # I'm assuming these values are Unicode
    terms.append(SimpleTerm(value,
                                token=value.encode('unicode_escape'), title=value))
    return SimpleVocabulary(terms)
    
class IOrgnization_annual_survey(form.Schema,IBasic):

##所属社会组织
#    title = schema.Choice(
#            title=_(u"organization name"),
#            source=DynamicVocabulary("my315ok.socialorgnization.content.orgnization", "IOrgnization",name="title")
#                        ) 
    title = schema.Choice(
        title=_(u"organization name"),     
        source=possibleOrganization,     
        required=True
    )
# 上级主管单位
    sponsor = schema.Text(title=_(u"sponsor"), required=False)
# 上级主管单位意见    
    sponsor_comments = schema.Text(title=_(u"sponsor comments"), required=False)
# 民政局意见      
    agent_comments = schema.Text(title=_(u"civil agent comments"), required=False)    
   
# 上级主管单位审核日期 
    sponsor_audit_date = schema.Text(title=_(u"sponsor audit date"), required=False)
# 民政局审核日期      
    agent_audit_date = schema.Text(title=_(u"civil agent audit date"), required=False) 
    
#年度           
    year = schema.TextLine(title=_(u"the year for survey"),
                             default=u"2012",
                             required=False,)

#年检报告书    
    report = NamedBlobFile(title=_(u"report"),
        description=_(u"Attach your anual report (word, etc)."),
        required=True
    )
# 上次工作流状态
    last_status = schema.TextLine(title=_(u"last status of the annual survey"),                             
                             required=False,)
    
#年检结果            
    annual_survey = schema.Choice(
        title=_(u"the result of annual survey"),
        vocabulary="my315ok.socialorgnization.vocabulary.annualsurvey"
    )       
# 审核历史

#    traced_history = schema.Text(title=_(u"traced history"), required=False)     
    
    form.omitted('description','sponsor','sponsor_comments','sponsor_audit_date','agent_audit_date','agent_comments','last_status','annual_survey')    

class IOrgnization_administrative_licence(form.Schema,IBasic):

##所属社会组织
#    title = schema.Choice(
#            title=_(u"organization name"),
#            source=DynamicVocabulary("my315ok.socialorgnization.content.orgnization", "IOrgnization",name="title")
#                        )
    title = schema.Choice(
        title=_(u"organization name"),     
        source=possibleOrganization,     
        required=True
    )
#许可事项            
    audit_item = schema.Choice(
        title=_(u"the item had been audited"),
        vocabulary="my315ok.socialorgnization.vocabulary.audit_item"
    )
    
#结果          
    audit_result = schema.Choice(
                                 title=_(u"the result of item that had been audited"),
                                 vocabulary="my315ok.socialorgnization.vocabulary.audit_result",                                 
                                 default="zhunyu",
                                 required=False,)
    audit_date = schema.Date(
        title=_(u"Pass Date"),
        description=u'',
        required=False,
    )
     
    form.omitted('description')       
    
@form.default_value(field=IOrgnization['passDate'])
def passDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(-1)  

@form.default_value(field=IOrgnization_annual_survey['year'])
def surveyYearDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return (datetime.datetime.today() + datetime.timedelta(-365)).strftime("%Y") 

@form.default_value(field=IOrgnization_administrative_licence['audit_date'])
def auditdateDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(-10)           