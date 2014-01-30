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
    return rdf

def convert(rdf):
    data = urllib.urlencode({"format":"OWL/RDF","ontology":rdf})
    url = "http://mowl-power.cs.man.ac.uk:8080/converter/convert"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'39969',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'JSESSIONID=2373189D4117A290C8CA32A210103A6A; __utma=51512245.292168978.1391095601.1391095601.1391095601.1; __utmc=51512245; __utmz=51512245.1391095601.1.1.utmccn=(referral)|utmcsr=answers.semanticweb.com|utmcct=/questions/1486/are-there-any-owl-to-rdfxml-converters|utmcmd=referral; __utmb=51512245',
        'Host':'mowl-power.cs.man.ac.uk:8080',
        'Origin':'http://mowl-power.cs.man.ac.uk:8080',
        'Referer':'http://mowl-power.cs.man.ac.uk:8080/converter/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'
        }
    u = urllib.urlopen(url,data,headers)
    #u = urllib.urlopen("http://mowl-power.cs.man.ac.uk:8080/converter/convert", data)
    response = ""
    while 1:
        data = u.read()
        if not data:
            break
        response += data

    return response
