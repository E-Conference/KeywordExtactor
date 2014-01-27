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
    return hierarchiser.go()

@app.route('/clusters/<int:kw_number>/<int:cluster_number>')
def clusters(kw_number, cluster_number):
    return clustering.clusterIt(kw_number, cluster_number)

if __name__ == '__main__':
    app.run(debug = True)
