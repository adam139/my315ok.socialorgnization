# -*- coding: UTF-8 -*-

from my315ok.socialorgnization.content.orgnization import ICostomTitle
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from plone.app.content.interfaces import INameFromTitle
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface


def get_title_from_parent(context):
    """根据父对象id，获得对象title"""

    parent = context.getParentNode()
    title = parent.title
    if title != "":
        return title
    else:
        return parent.id


class INameFromParentId(INameFromTitle):
    """Get the name from parent object's id.
    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class NameFromParentId(object):
    implements(INameFromParentId)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        #         import pdb
        #         pdb.set_trace()
        return get_title_from_parent(self.context)
