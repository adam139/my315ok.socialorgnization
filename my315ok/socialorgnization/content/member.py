# -*- coding: utf-8 -*-
from my315ok.socialorgnization import _
from dexterity.membrane.content.member import IMember
from zope.interface import implementer
from zope import schema
from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary,FirstDynamicVocabulary
from my315ok.socialorgnization.content.orgnization import IOrgnization
   
### organization membe
inlist = ["市民政局","市科协","市社科联","市文联","市工商联"]
class IOrganizationMember(IMember):
    """
    Organization Member
    """    

#     inlist = ["市民政局","市科协","市社科联","市文联","市工商联"]
#     orgname = schema.Choice(
#              title=_(u"organization name"),
#              source=FirstDynamicVocabulary("my315ok.socialorgnization.content.orgnization",
#                                       "IOrgnization",inlist,
#                                       orgnization_belondtoArea="xiangtanshi")
#                          )  
### organization sponsor member
class ISponsorMember(IMember):
    """
    Government department Member
    """
    pass
  
#     orgname = schema.Choice(
#             title=_(u"Government department"),
#             source=DynamicVocabulary("my315ok.socialorgnization.content.governmentdepartment", "IOrgnization")
#                         )     


    