# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from five import grok
from my315ok.socialorgnization import _
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.directives import form


class IPage(form.Schema):
    """
    a page content that contain rich text.
    """

#     dexteritytextindexer.searchable('text')
    text = RichText(
        title=_(u"body text"),
        required=True,
    )


class Page(dexterity.Item):
    grok.implements(IPage)
