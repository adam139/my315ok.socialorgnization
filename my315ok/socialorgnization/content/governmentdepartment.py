#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
import datetime

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary
from plone.namedfile.field import NamedBlobImage

from collective import dexteritytextindexer

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
#from collective.dexteritytextindexer.behavior import IDexterityTextIndexer

from my315ok.socialorgnization import _

class IOrgnization(form.Schema,IImageScaleTraversable):
    """
    内容类型接口，注册为：my315ok.socialorgnization.governmentorgnization
    政府部门单位：市教育局等
    """
#名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"orgnization name"),
                             default=u"",
                            required=True,) 
#描述       
    description = schema.TextLine(title=_(u"sector"),
                             default=u"",
                             required=False,)
#   住所 
    address = schema.TextLine(title=_(u"Address"),
                             default=u"",
                             required=False,)
#   经手人 
    operator = schema.TextLine(title=_(u"operator"),
                             default=u"",
                             required=False,)
    
#   公章     
    image = NamedBlobImage(title=_(u"public sign"),
                             description=_(u"a image of the public sign"),
                             required=False,)


@grok.provider(IContextSourceBinder)
def possibleOrganization(context):
         

    terms = []
    value = context.title  # I'm assuming these values are Unicode
    terms.append(SimpleTerm(value,
                                token=value.encode('unicode_escape'), title=value))
    return SimpleVocabulary(terms)
    
        