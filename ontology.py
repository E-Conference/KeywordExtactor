# -*- coding: utf-8 -*-
import urllib
import urllib2
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DC, FOAF, OWL

def escape(kw):
    kw = kw.replace(u"”","")
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
    rdf = rdf.replace('<?xml version="1.0" encoding="UTF-8"?>','')
    owl = convert(rdf)
    return owl

def convert(rdf):
    data = urllib.urlencode({"format":"OWL/XML","ontology":rdf})
    url = "http://mowl-power.cs.man.ac.uk:8080/converter/convert"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {        
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }
    #u = urllib.urlopen(url,data,headers)
    u = urllib.urlopen("http://mowl-power.cs.man.ac.uk:8080/converter/convert", data)
    response = ""
    while 1:
        data = u.read()
        if not data:
            break
        response += data

    return response
