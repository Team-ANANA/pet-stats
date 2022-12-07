import dateutil.parser
from flask import Flask, jsonify, make_response, request
from datetime import datetime
import sql_util
import logging
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

param_names=['type', 'age', 'breed', 'gender', 'size', 'status', 'country', 'state']

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('api.log'), logging.StreamHandler()])

@app.get('/')
def default_route():
    return 'This is the root directory.'

# Route for querying entries for all parameters
@app.get('/V0/data/entry')
@cross_origin()
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
@cross_origin()
def get_pie_graph():

    # list of parameters in query
    parameters = request.get_json()
    logging.info("Received pie graph request with body: %s", str(parameters))

    # category is mandatory for pie graph request
    if 'category' in parameters:
        category = parameters['category']
        category = category.lower()
    else:
        logging.debug("BAD REQUEST: missing category for pie graph.")
        return make_response("", 400)
    if category not in param_names:
        logging.debug("BAD REQUEST: invalid category for pie graph.")
        return make_response("", 400)
        
    # parse the tables for where conditions
    where = "WHERE "
    sql_array = []

    # only add condition if parameter is given
    for param_name, entries in parameters.items():
        if entries != []:
            if param_name == 'breed':
                # need two temp breed tables for query
                sql_array.extend(sql_util.create_temp_table(entries, param_name).split(";"))
                sql_array.extend(sql_util.create_temp_table(entries, param_name + '_two').split(";"))
                where += f"((primary_breed_id IN (SELECT id FROM temp_breed)) \
                        OR (secondary_breed_id IN (SELECT id from temp_breed_two))) AND "
            elif param_name not in ['dateEnd', 'dateBegin', 'gender', 'category']:
                sql_array.extend(sql_util.create_temp_table(entries, param_name).split(";"))
                if param_name == 'type':
                    # need two temp type tables for query
                    sql_array.extend(sql_util.create_temp_table(entries, param_name + '_two').split(";"))
                where += f"({param_name}_id IN (SELECT id FROM temp_{param_name})) AND "

            GENDERS = {1: "Female", 2: "Male", 3: "Unknown"}
            if param_name == 'gender':
                # No need to add gender query if all genders are selected
                if len(entries) != 3:
                    genders = []
                    for gender_id in entries:
                        genders.append(GENDERS[gender_id])
                    sql_array.extend(sql_util.create_temp_table(genders, "gender").split(";"))
                    where += f"(gender_id IN (SELECT id FROM gender WHERE ((gender.type_id IN (SELECT id FROM temp_type_two)) AND (gender.descriptor IN (SELECT id FROM temp_gender))))) AND "        

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = dateutil.parser.parse(parameters['dateBegin'])
        end = dateutil.parser.parse(parameters['dateEnd'])
        where += f"(DATE(published_at) BETWEEN '{begin}' AND '{end}')"
    else:
        logging.debug("BAD REQUEST: missing dateBegin or dateEnd for pie graph.")
        return make_response("", 400)
    
    if category == 'type':
        descriptor = 'type.name'
    else:
        descriptor = f"{category}.descriptor"

    # construct the final sql statement.
    sql = f"SELECT count, {descriptor} from ((SELECT COUNT(id) as count, {category}_id " \
        +  "FROM animals "\
        + where\
        + f"GROUP BY {category}_id " \
        + f") AS base INNER JOIN {category} ON {category}_id = {category}.id);"

    # clean up sql
    sql_array.append(sql)

    data = sql_util.execute_multiple_sql(sql_array)

    reformatted_data = {}
    for count, category in data:
        reformatted_data[category] = count
    
    logging.debug("Pie Graph data collected: %s", str(reformatted_data))
    
    return make_response(jsonify(reformatted_data), 200)

# Route for querying for heatmap
@app.post('/V0/graph/heat')
@cross_origin()
def get_heat_map():

    # list of parameters in query
    parameters = request.get_json()
    logging.info("Received heatmap request with body: %s", str(parameters))

    # country is mandatory for pie graph request
    if 'country' in parameters:
        country = parameters['country']
    else:
        logging.debug("Missing country parameter in heatmap request.")
        return make_response("", 400)
    
    # parse the tables for where conditions
    where = "WHERE"
    sql_array = []


    
    # only add condition if parameter is given
    for param_name, entries in parameters.items():
        if entries != []:
            if param_name == 'breed':
                # need two temp breed tables for query since temp table can't be referenced twice
                sql_array.extend(sql_util.create_temp_table(entries, param_name).split(";"))
                sql_array.extend(sql_util.create_temp_table(entries, param_name + '_two').split(";"))
                where += f"((primary_breed_id IN (SELECT id FROM temp_breed)) \
                        OR (secondary_breed_id IN (SELECT id from temp_breed_two))) AND "
            elif param_name not in ['dateEnd', 'dateBegin', 'gender', 'state', 'country']:
                sql_array.extend(sql_util.create_temp_table(entries, param_name).split(";"))
                if param_name == 'type':
                    # need two temp type tables, one for type_id, one for gender
                    sql_array.extend(sql_util.create_temp_table(entries, param_name + '_two').split(";"))
                where += f"({param_name}_id IN (SELECT id FROM temp_{param_name})) AND "

            GENDERS = {1: "Female", 2: "Male", 3: "Unknown"}
            if param_name == 'gender':
                # No need to add gender query if all genders are selected
                if len(entries) != 3:
                    genders = []
                    for gender_id in entries:
                        genders.append(GENDERS[gender_id])
                    sql_array.extend(sql_util.create_temp_table(genders, "gender").split(";"))
                    where += f"(gender_id IN (SELECT id FROM gender WHERE ((gender.type_id IN (SELECT id FROM temp_type_two)) AND (gender.descriptor IN (SELECT id FROM temp_gender))))) AND "
    
    countries = {"USA":1, "Canada": 2}
    # add country condition
    where += f"(country_id = {countries[country]}) AND"

    # add date range in query
    if 'dateBegin' in parameters and 'dateEnd' in parameters:
        begin = dateutil.parser.parse(parameters['dateBegin'])
        end = dateutil.parser.parse(parameters['dateEnd'])
        where += f"(DATE(published_at) BETWEEN '{begin}' AND '{end}') "
    else:
        logging.debug("BAD REQUEST: missing dateBegin or dateEnd for heatmap.")
        return make_response("", 400)

    # construct the final sql statement.
    sql = f"SELECT COUNT(id), province " \
        +  "FROM (SELECT animals.*, state.descriptor as province FROM animals INNER JOIN state ON animals.state_id = state.id) as joined_table "\
        + where + f"GROUP BY province"

    sql_array.append(sql)

    # execute sql query
    data = sql_util.execute_multiple_sql(sql_array)

    # format payload in province to number of matching animals mapping
    reformatted_data = {}
    for count, province in data:
        reformatted_data[province] = count
    
    return make_response(jsonify(reformatted_data), 200)
    
