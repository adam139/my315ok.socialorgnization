from five import grok
from my315ok.socialorgnization import _
from plone.directives import dexterity
from plone.directives import form
from zope import schema


class IAnnualSurveyFolder(form.Schema):
    """
    a folder contain some annual survey information for social organizations
    """
