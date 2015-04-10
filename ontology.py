# -*- coding: utf-8 -*-
import urllib
import urllib2
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DC, FOAF, OWL

def escape(kw):
    kw = kw.replace(u"”", "")
    kw = kw.replace(u"“", "")
    kw = kw.replace(" ", "+")
    return kw

def generate(bag, uri):
    g = Graph()
    keywords_xml = URIRef(uri)    
    n = Namespace(uri)
    g.add( (keywords_xml, RDF.type, RDFS.Class) )    
    for keywords in bag:
        for keyword in keywords:            
            g.add ( (URIRef(uri + escape(keyword.keyword)), RDFS.Class, keywords_xml) )
            if (keyword.father != None):
                g.add ( (URIRef(uri + escape(keyword.keyword)), RDFS.subClassOf, URIRef(uri + escape(keyword.father.keyword)) ))
            g.add( (URIRef(uri + escape(keyword.keyword)), DC.subject, URIRef(keyword.uri)))
    rdf = g.serialize(format='application/rdf+xml')
    return rdf
