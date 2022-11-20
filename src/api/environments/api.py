from flask import Flask, jsonify, make_response, request
from datetime import datetime
import sql_util
import logging

app = Flask(__name__)
param_names=['type', 'age', 'breed', 'gender', 'size', 'status', 'country', 'province']

logging.basicConfig(filename='api.log', encoding='utf-8', level=logging.DEBUG)

@app.get('/')
def default_route():
    return 'This is the root directory.'

# Route for querying entries for all parameters
@app.get('/V0/data/entry/')
def get_entries():
    entries = {}
    types = {}
    countries = {}

    # query each enum table and store them in entries
    for param in param_names:
        sql = f"SELECT * FROM {param};"
        data = sql_util.execute_sql(sql)
        rows = {}

        # get mapping of type and country for breed and province
        if param == 'type':
            for id,type in data:
                types[id] = type
        elif param == 'country':
            for id,country in data:
                countries[id] = country

        if param == "breed":
            for id, type_id, breed in data:
                type = types[type_id]
                if type not in rows:
                    rows[type] = {}
                rows[type][breed] = id
        elif param == "province":
            for id, country_id, province in data:
                country = countries[country_id]
                if country not in rows:
                    rows[country] = {}
                rows[country][province] = id
        else:
            for id, entry in data:
                rows[entry] = id
        entries[param]=rows

    return make_response(jsonify(entries), 200)


# Route for querying for pie graph
@app.post('/V0/graph/pie')
def get_pie_graph():

    # list of parameters in query
    parameters = request.get_json()
    logging.info("Received pie graph request with body: %s", str(parameters))

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
            temp_table += sql_util.create_temp_table(entries, param_name)
            where += f"({param_name} in (SELECT * FROM @{param_name})) AND"

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = datetime.strptime(parameters['dateBegin'], '%Y-%m-%d')
        where += f"(published_at >= {begin}) AND"
        end = datetime.strptime(parameters['dateEnd'], '%Y-%m-%d')
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
    data = sql_util.execute_sql(sql)

    reformatted_data = {}
    for count, category in data:
        reformatted_data[category] = count
    
    return make_response(jsonify(reformatted_data), 200)

