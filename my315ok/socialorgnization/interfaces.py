# -*- coding: UTF-8 -*-
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface


# event


class ICreateOrgEvent(Interface):
    """新增一个organization object"""
