#!flask/bin/python
from flask import Flask
import hierarchiser
import combinaison
import clustering

app = Flask(__name__)

@app.route('/kw/<int:number>')
def kw(number):
    return combinaison.launch(number)

@app.route('/')
def index():    
    return "nothing to do here"

@app.route('/clusters/<int:kw_number>/<int:cluster_number>')
def clusters(kw_number, cluster_number):
    return clustering.clusterIt(kw_number, cluster_number)

@app.route('/hierarchy/<int:kw_number>/<int:cluster_number>')
def hierarchy(kw_number, cluster_number):
    clusters = clustering.clusterIt(kw_number, cluster_number)
    return hierarchiser.go(clusters)

if __name__ == '__main__':
    app.run(debug = True)
