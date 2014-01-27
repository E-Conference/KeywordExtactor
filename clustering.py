import sys
import combinaison
import numpy
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance
import nltk.corpus
from nltk import decorators
import nltk.stem
 
stemmer_func = nltk.stem.snowball.EnglishStemmer().stem
stopwords = set(nltk.corpus.stopwords.words('english'))

def clusterIt(kwnb, clusternb):
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

    
    keywords = combinaison.launch(kwnb)
    ret = ""
    job_titles = [line.strip() for line in keywords.split("<br/>")]
    job_titles = [x.decode('windows-1252') for x in job_titles]
    job_titles = [x.encode('ascii', 'ignore') for x in job_titles]

    words = get_words(job_titles)

    # cluster = KMeansClusterer(5, euclidean_distance)
    cluster = GAAClusterer(clusternb)
    cluster.cluster([vectorspaced(title) for title in job_titles if title])
    classified_examples = [cluster.classify(vectorspaced(title)) for title in job_titles]
    
    for cluster_id, title in sorted(zip(classified_examples, job_titles)):
        ret = ret + (str(cluster_id) + ";" + str(title) + "<br/>")
    return ret
