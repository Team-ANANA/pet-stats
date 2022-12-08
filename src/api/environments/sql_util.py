import mysql.connector
import logging

def execute_sql(sql):
    data = {}
    try:
        logging.debug("Executing SQL: %s", sql)
        cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                                    host='172.17.0.2',
                                    database='pet-stats')
        mycursor = cnx.cursor()
        mycursor.execute(sql)
        data = mycursor.fetchall()
        cnx.close()
    except Exception as e:
        logging.error("MySQL Error: %s", str(e))
    return data

def execute_multiple_sql(sql_array):
    data = {}
    try:
        logging.debug("Executing SQL: %s", str(sql_array))
        # use localhost when not running inside a docker container
        # cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
        #                             host='localhost',
        #                             database='pet-stats')

        # use docker container ip address when running inside docker container
        cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                                    host='172.17.0.2',
                                    database='pet-stats')
        mycursor = cnx.cursor()
        for sql in sql_array:
            mycursor.execute(sql)
            data = mycursor.fetchall()
        cnx.close()
    except Exception as e:
        logging.error("MySQL Error: %s", str(e))
    return data

def create_temp_table(array, table_name):
    values = ""
    for entry in array:
        if table_name != 'gender':
            values += f",({entry})"
        else:
            values += ",('" + entry + "')"
    values = values[1:]
    sql = f"CREATE TEMPORARY TABLE temp_{table_name} (id varchar(100));INSERT INTO temp_{table_name} (id) VALUES {values}" 
    return sql
    
