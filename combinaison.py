import rake_adapted
import rake
import re
import MySQLdb
import re
import operator
import math
from datetime import datetime, time

def MySQLDoc():
    db = MySQLdb.connect(host="127.0.0.1", user="wwwConf", passwd="dataconfTER", db="livecon", port=3306)
    #db = MySQLdb.connect(host="localhost", user="root", passwd="", db="wwwconference")
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM paper WHERE length(abstract)>150")
    for row in cur.fetchall():
        max_size = int(row[0])

    print str(max_size) + " docs."

    documents = [None] * max_size

    cur.execute("SELECT title,abstract FROM paper WHERE length(abstract)>150")

    i = 0
    for row in cur.fetchall() :
        documents[i] = str(row[0])+" "+str(row[1])
        i = i+1
    return [' '.join(documents)]

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
    return not("_" in kw_t[0])

def NotStopWord(kw_t, wordlist):
    for subkw in kw_t[0].split(" "):        
        if subkw in open(wordlist).read():
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
            if lenK < 4 :
                if HasNoNum(kw) & HasHigherScoreThan(kw) & x_EdCheck(kw) & HasUnique(kw[0],currentArray) & specialCharsCheck(kw) & NotStopWord(kw, "LongStopList.txt"):
                    currentArray.append(kw)
        finalArray.append(currentArray)
    return finalArray

def launch(kwnb):
    ret = ""
    documents = MySQLDoc()
    dockws = FilteringKw(documents)
    i=0

    for dockw in list(dockws):        
        i+=1                
        j=0
        for kw in sorted(dockw, key=operator.itemgetter(1), reverse=True):            
            if j<kwnb:                
                ret = ret + str(kw[0]) + ";" + str(kw[1]) + "<br/>"
                j+=1
            else:
                break        
        return ret
