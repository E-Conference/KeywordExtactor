import sys
import combinaison
import numpy
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance
import nltk.corpus
from nltk import decorators
import nltk.stem
#import keyword
 
stemmer_func = nltk.stem.snowball.EnglishStemmer().stem
stopwords = set(nltk.corpus.stopwords.words('english'))

def clusterAll(kwnb, clusternb, conf_uri):
    bag = combinaison.launch(kwnb, conf_uri)
    final = list()
    for keywords in bag:
        final.append(clusterIt(kwnb, clusternb, keywords))
    return final

def clusterIt(kwnb, clusternb, keywords):
    @decorators.memoize
    def normalize_word(word):
        return stemmer_func(word.lower())
     
    def get_words(titles):
        words = set()
        for title in job_titles:                        
                for word in title.split():
                    words.add(normalize_word(word))
        return list(words)
     
    @decorators.memoize
    def vectorspaced(title):
        title_components = [normalize_word(word) for word in title.split()]
        return numpy.array([
            word in title_components and not word in stopwords
            for word in words], numpy.short)
    
    ret = list()          
    if len(keywords) > 0:                        
        job_titles = [x.keyword for x in keywords]
        job_titles = [x.strip() for x in job_titles]
        words = get_words(job_titles)    
        
        # cluster = KMeansClusterer(5, euclidean_distance)
        cluster = GAAClusterer(clusternb)
        cluster.cluster([vectorspaced(title) for title in job_titles if title])
        classified_examples = [cluster.classify(vectorspaced(title)) for title in job_titles]
        
        for cluster_id, title in sorted(zip(classified_examples, job_titles)):
            if(title != ''):
                for keyword in keywords:
                    if (title==keyword.keyword):
                        keyword.assignCluster(cluster_id)
                        ret.append(keyword)
    return ret
