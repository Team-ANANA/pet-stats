from flask import Flask, jsonify, make_response, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)
param_names=['type', 'age', 'breed', 'gender', 'size', 'status', 'country', 'province']

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
    
    cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                                host='localhost',
                                database='pet-stats')
    mycursor = cnx.cursor()
    # query each enum table and store them in entries
    for param in param_names:
        sql = f"SELECT * FROM {param} "
        mycursor.execute(sql)
        data = mycursor.fetchall()
        rows = {}
        if param == "breed" or param == "province":
            for id, parent_id, child_name in data:
                rows[parent_id][child_name] = id
        else:
            for id, entry in data:
                rows[entry] = id
        entries[param]=rows
    cnx.close()    
    return make_response(jsonify(entries), 200)


# Route for querying for pie graph
@app.post('/V0/graph/pie')
def get_pie_graph():
    # list of parameters in query
    parameters = request.get_json()

    # category is mandatory for pie graph request
    if 'category' in parameters:
        category = parameters['category']
    else:
        return make_response("", 400)
    if category not in param_names:
        return make_response("", 400)
        
    # parse the tables for where conditions
    where = "Where "
    temp_table = ""
    
    # only add condition if parameter is given
    for param_name, entries in parameters.items():
        if entries != [] and param_name not in ['dateEnd', 'dateBegin']:
            temp_table += create_temp_table(entries, param_name)
            where += f"({param_name} in (SELECT * FROM @{param_name})) AND"

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = datetime.strptime(parameters['dateBegin'])
        begin = datetime.timestamp(begin)
        where += f"(published_at >= {begin}) AND"
        end = datetime.strptime(parameters['dateEnd'])
        end = datetime.timestamp(end)
        where += f"(published_at <= {end}"
    else:
        return make_response("", 400)

    # construct the final sql statement.
    sql = temp_table \
        + f"SELECT COUNT(id), {category}" \
        +  "FROM animals"\
        + f"GROUP BY {category}" \
        + where + ";"

    # execute sql query
    cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                                host='localhost',
                                database='pet-stats')
    mycursor = cnx.cursor()
    mycursor.execute(sql)
    data = mycursor.fetchall()
    cnx.close()
    
    return make_response(jsonify(data), 200)

def create_temp_table(array, table_name):
    values = ""
    for entry in array:
        values += f",({entry})"
    values = values[1:]
    sql = f"""
    DECLARE @{table_name} varchar(100);
    INSERT INTO @{table_name} values{values};
    """ 
    return sql
    
