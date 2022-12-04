import mysql.connector
from logging import error

def execute_sql(sql):
    data = {}
    try:
        cnx = mysql.connector.connect(user='root', password='my-secret-pw', port="3306",
                                    host='localhost',
                                    database='pet-stats')
        mycursor = cnx.cursor()
        mycursor.execute(sql)
        data = mycursor.fetchall()
        cnx.close()
    except mysql.connector.Error as e:
        error("MySQL Error: %s", str(e))
    return data

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
    
