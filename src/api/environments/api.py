from flask import Flask, jsonify, make_response, request
from datetime import datetime
import sql_util
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

param_names=['type', 'age', 'breed', 'gender', 'size', 'status', 'country', 'state']

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('api.log'), logging.StreamHandler()])

@app.get('/')
def default_route():
    return 'This is the root directory.'

# Route for querying entries for all parameters
@app.get('/V0/data/entry')
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
            for id, type_id, descriptor in data:
                type = types[type_id]
                if type not in rows:
                    rows[type] = {}
                rows[type][descriptor] = id
        elif param == "state":
            for id, country_id, province in data:
                country = countries[country_id]
                if country not in rows:
                    rows[country] = {}
                rows[country][province] = id
        elif param == "gender":
            rows["Female"] = 1
            rows["Male"] = 2
            rows["Unknown"] = 3
        else:
            for id, entry in data:
                rows[entry] = id
        entries[param.capitalize()]=rows 

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
        if entries != [] and param_name not in ['dateEnd', 'dateBegin', 'country']:
            temp_table += sql_util.create_temp_table(entries, param_name)
            where += f"({param_name} in (SELECT * FROM @{param_name})) AND"

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = datetime.strptime(parameters['dateBegin'], '%Y-%m-%d')
        where += f"(published_at >= {begin}) AND"
        end = datetime.strptime(parameters['dateEnd'], '%Y-%m-%d')
        where += f"(published_at <= {end})"
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

# Route for querying for heatmap
@app.post('/V0/graph/heat')
def get_heat_map():

    # list of parameters in query
    parameters = request.get_json()
    logging.info("Received heatmap request with body: %s", str(parameters))

    # country is mandatory for pie graph request
    if 'country' in parameters:
        country = parameters['country']
    else:
        return make_response("", 400)
    
    # parse the tables for where conditions
    where = f"WHERE"
    temp_table = ""
    
    # only add condition if parameter is given
    for param_name, entries in parameters.items():
        if entries != [] and param_name not in ['dateEnd', 'dateBegin']:
            temp_table += sql_util.create_temp_table(entries, param_name)
            if param_name == 'breed':
                where += f"((primary_breed_id IN (SELECT * FROM @{param_name})) OR \
                            (secondary_breed_id IN (SELECT * FROM @{param_name}))) AND"
            else:
                where += f"({param_name}_id IN (SELECT * FROM @{param_name})) AND"

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = datetime.strptime(parameters['dateBegin'], '%Y-%m-%d')
        where += f"(published_at >= {begin}) AND"
        end = datetime.strptime(parameters['dateEnd'], '%Y-%m-%d')
        where += f"(published_at <= {end})"
    else:
        return make_response("", 400)

    # construct the final sql statement.
    sql = temp_table \
        + f"SELECT COUNT(animals.id), province.descriptor" \
        +  "FROM (animals INNER JOIN province ON animals.province_id = province.id)"\
        + f"GROUP BY province_id" \
        + where + ";"

    # execute sql query
    data = sql_util.execute_sql(sql)

    # format payload in province to number of matching animals mapping
    reformatted_data = {}
    for count, province in data:
        reformatted_data[province] = count
    
    return make_response(jsonify(reformatted_data), 200)
    
