# -*- coding: utf-8 -*-
from five import grok
from plone.directives import dexterity, form
from plone.multilingualbehavior import directives
from zope import schema
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from my315ok.socialorgnization import _
   
class IPage(form.Schema):
    """
    a page content that contain rich text.
    """

    dexteritytextindexer.searchable('text')  
    text = RichText(
            title=_(u"body text"),
            required=True,
        )



class Page(dexterity.Item):
    grok.implements(IPage)


