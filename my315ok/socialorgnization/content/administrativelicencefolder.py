from five import grok
from my315ok.socialorgnization import _
from plone.directives import dexterity
from plone.directives import form
from zope import schema


class IAdministrativeLicenceFolder(form.Schema):
    """
    a folder contain some administrative licence information for social organizations
    """
