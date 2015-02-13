from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from five import grok
from Products.CMFCore.utils import getToolByName

from my315ok.socialorgnization import _

class RegistrySource(object):
    """build source from registry values
    """
    grok.implements(IContextSourceBinder)
    
    def __init__(self,key):
        self.key = key
    
    def __call__(self,context):
        registry = queryUtility(IRegistry)
        terms = []
        vdict = registry.get(self.key,{})
        vkeys = sorted(vdict.keys())
        if registry is not None:
               for index in vkeys: 
                   value = vdict.get(index)
                   terms.append(SimpleVocabulary.createTerm(index,value,_(value)))
        return SimpleVocabulary(terms)
    
    def getKeys(self):
        registry = queryUtility(IRegistry)
        return sorted(registry.get(self.key,{}).keys())
    
    def getDict(self):
        registry = queryUtility(IRegistry)
        d = registry.get(self.key,{})
        for k in d:
            d[k] = _(d[k])
        return d
    
    def getValue(self,num):
        registry = queryUtility(IRegistry)
        if registry is not None:
            return  _(registry.get(self.key,{}).get(num))

class DynamicVocabulary(object):
    grok.implements(IContextSourceBinder)
    
    def __init__(self,key,mo,**kw):
        """key:package name;mo:content object interface;
        kw as catalog search condition"""
        self.key = key
        self.mo = mo
        self.query = kw
        
    def __call__(self,context):
        terms = []
#        import pdb
#        pdb.set_trace()
        exec("from %s import %s as mo"%(self.key,self.mo))
        catalog = getToolByName(context,"portal_catalog")
        if mo:
            self.query.update({"object_provides":mo.__identifier__})                
            all = catalog.unrestrictedSearchResults(self.query)
            for bs in all:
                title = bs.Title
                id = bs.id
                terms.append(SimpleVocabulary.createTerm(id,id,title))
        return SimpleVocabulary(terms)

