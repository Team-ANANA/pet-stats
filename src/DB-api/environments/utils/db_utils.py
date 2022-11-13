import mysql.connector
from pathlib import Path


def get_db_config():
    # TODO setup env variables to hide password etc
    return {'user':'root', 'password':'my-secret-pw', 'port':"3306",
                              'host':'localhost',
                              'database':'pet-stats'}

def execute_migration(migration):
    cnx = mysql.connector.connect(**get_db_config())
    cursor = cnx.cursor()
    migration_path = Path(__file__).parent.parent / 'migrations' / f'{migration}'
    fd = open(migration_path, 'r')
    migration_file = fd.read()
    fd.close()
    migration_operations = migration_file.replace('\n', '').split(';')


    # execute migration operations
    for operation in migration_operations:
        cursor.execute(operation)
