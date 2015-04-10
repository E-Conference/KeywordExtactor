#!flask/bin/python
from flask import Flask
import hierarchiser
import combinaison
import clustering
import ontology
from flask import Response
from flask import request
from datetime import datetime, time

app = Flask(__name__)

@app.route('/')
def index():    
    return "nothing to do here"

@app.route('/onto/<int:knb>/<int:cnb>')
def onto(knb, cnb):
    
    now = datetime.now()
    beginning_of_day = datetime.combine(now.date(), time(0))
    
    iri = request.args['iri']    
    clusters = clustering.clusterAll(knb, cnb, iri)
    bag = list()
    ret = ""    
    for cluster in clusters:
        hierarchy = hierarchiser.go(cluster)
        bag.append(hierarchy)
    print (now - beginning_of_day).seconds
    response = Response(ontology.generate(bag, "http://data.live-con.com/resource/keyword#"), mimetype='text/xml')
    return response

if __name__ == '__main__':
    app.run(debug = True)
