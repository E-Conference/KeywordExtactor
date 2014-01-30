#!flask/bin/python
from flask import Flask
import hierarchiser
import combinaison
import clustering
import ontology
from flask import Response

app = Flask(__name__)

@app.route('/')
def index():    
    return "nothing to do here"

@app.route('/onto/<int:kw_number>/<int:cluster_number>')
def onto(kw_number, cluster_number):
    clusters = clustering.clusterAll(kw_number, cluster_number)
    bag = list()
    ret = ""    
    for cluster in clusters:
        hierarchy = hierarchiser.go(cluster)
        bag.append(hierarchy)
    return Response(ontology.generate(bag, "http://data.live-con.com/resource/keyword/"), mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug = True)
