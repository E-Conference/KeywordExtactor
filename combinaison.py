# -*- coding: utf-8 -*-
import rake_adapted
import rake
from os import sys
import re
import MySQLdb
import re
import operator
import math
import codecs
from datetime import datetime, time
from BeautifulSoup import BeautifulSoup 
import urllib, urllib2

##def MySQLDoc():
##    db = MySQLdb.connect(host="127.0.0.1", user="wwwConf", passwd="dataconfTER", db="livecon", port=3306)
##    #db = MySQLdb.connect(host="localhost", user="root", passwd="", db="wwwconference")
##    cur = db.cursor()
##
##    cur.execute("SELECT COUNT(*) FROM paper WHERE length(abstract)>150")
##    for row in cur.fetchall():
##        max_size = int(row[0])
##
##    print str(max_size) + " docs."
##
##    documents = [None] * max_size
##
##    cur.execute("SELECT title,abstract FROM paper WHERE length(abstract)>150")
##
##    i = 0
##    for row in cur.fetchall() :
##        documents[i] = str(row[0])+" "+str(row[1])
##        i = i+1
##    return [' '.join(documents)]

class PaperUri:
    uri_conf = ""
    abstracts = list()
    
    def __init__(self, uri, abs):
        self.uri_conf = uri
        self.abstract = abs

    def addAbstract(self, abs):
        self.abstracts.append(abs)

    def getFirstAbs(self):
        for abs in self.abstract:
            return abs

class Keyword:
    uri = ""
    keyword = ""
    score = ""
    cluster = 0
    father = None

    def __init__(self, uri, keyword, score):
        self.uri = uri
        self.keyword = keyword
        self.score = score

    def assignCluster(self, cluster):
        self.cluster = cluster

    def assignFather(self, father):
        self.father = father

def SPARQL(conf_uri):
    url="http://data.live-con.com/sparql?query="    
    query="select ?a where { <" + conf_uri + "> swc:hasRelatedDocument?d. ?d swrc:abstract ?a }"
    prefixes = "PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX db: <http://data.live-con.com/resource/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX swrc-ext: <http://www.cs.vu.nl/~mcaklein/onto/swrc_ext/2005/05#> PREFIX meta: <http://www4.wiwiss.fu-berlin.de/bizer/d2r-server/metadata#> PREFIX dcterms: <http://purl.org/dc/terms/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX map: <http://data.live-con.com/resource/#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX swrc: <http://swrc.ontoware.org/ontology#> PREFIX ical: <http://www.w3.org/2002/12/cal/ical#> PREFIX vocab: <http://data.live-con.com/resource/vocab/> PREFIX swc: <http://data.semanticweb.org/ns/swc/ontology#>"
    query = prefixes + " " + query

    documents = PaperUri(conf_uri, list())
    xml = urllib2.urlopen(url + urllib.quote(query)).read()
    soup = BeautifulSoup(xml)    

    for literal in soup.findAll("literal"):
        documents.addAbstract(literal.string)            
    return documents

def combination(doc):
    kwre = rake.launch_re(doc, "./LongStopList.txt")
    kwnltk = rake_adapted.launch_nltk(doc)
    comb = kwnltk + kwre    
    return comb

def HasNoNum(kw):
    return not re.search('\d+', kw[0])

def HasHigherScoreThan(kw):
    return kw[1] > 1

def x_EdCheck(kw_t):
    return not(kw_t[0].endswith("ed") | kw_t[0].endswith("y"))

def x_IngCheck(kw_t):
    split = kw_t[0].split(" ");
    if(split[0].endswith("ing")):
       return 0
    return 1

def specialCharsCheck(kw_t):
    return (not("_" in kw_t[0]))

def NotStopWord(kw_t, wordlist):
    for subkw in kw_t[0].split(" "):        
        if subkw in codecs.open(wordlist, encoding='utf-8').read():
            return 0
    return 1

def OnlyKw(kws_t):
    array = []
    for kw_t in kws_t:
        array.append(kw_t[0])
    return array

def HasUnique(kw, kws_t):
    kws_t = OnlyKw(kws_t)    
    if kws_t.count(kw) > 0:
        return 0
    return 1

def FilteringKw(documents):
    finalArray = []
    for doc in documents:
        currentArray = []
        currentMoy = 0
        j = 0
        comb = combination(doc)
        comb = sorted(comb, key=operator.itemgetter(1))
        for kw in comb:
            kw = list(kw)            
            kw = tuple(kw)
            lenK = len(kw[0].split(" "))
            if lenK < 4:
                if HasNoNum(kw) & HasHigherScoreThan(kw) & x_EdCheck(kw) & HasUnique(kw[0],currentArray) & specialCharsCheck(kw) & NotStopWord(kw, "LongStopList.txt"):
                    currentArray.append(kw)
        finalArray.append(currentArray)
    return list(finalArray)

def NotIn(string, list):
    for keyword in list:
        if keyword.keyword == string:
            return False
    return True

def launch(kwnb, conf_uri):    
    documents = SPARQL(conf_uri)
    final = list()
    ret = list()        
    dockws = FilteringKw(documents.abstracts)
    j=0
    for dockw in dockws:        
        for kw in sorted(dockw, key=operator.itemgetter(1), reverse=True):            
            if j<kwnb:                                       
                if NotIn(kw[0],ret):
                    ret.append(Keyword(documents.uri_conf,kw[0],str(kw[1])))
                    j+=1
            else:
                break
    final.append(ret)
    return final
