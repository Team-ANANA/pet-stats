from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

@app.get('/')
def default_route():
    return 'This is the root directory. Try out the /hello route!'

@app.get('/hello')
def hello():
    return 'Hello, World!'

# Route for querying entries for all parameters
@app.get('V0/data/entry/')
def get_entries():

    entries = {}
    # TODO: fill in the entries with sql query
    return make_response(jsonify(entries), 200)


# Route for querying for pie graph
@app.post('/V0/graph/pie/<int:category>')
def get_pie_graph(category):
    if len(category) == 0:
        return make_response("", 400)
    
    # list of parameters to query with
    parameters = request.get_json()
    
    data = {}
    # TODO: fill in the data with sql query
    return make_response(jsonify(data), 200)
