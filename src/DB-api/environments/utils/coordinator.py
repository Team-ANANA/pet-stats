# script that runs the import and handles getting environment variables + making sure the Petfinder API is up
import os
import db_utils


def get_vars():

    vars = {
        "db_password": os.environ['PET_STATS_DB_PASSWORD'],
        "petfinder_payload": os.environ['PET_STATS_PETFINDER_PAYLOAD'],
    }
    if None in vars.values():
        # TODO use logging to do this
        print("unable to access environment variables")

    # TODO use logging to do this as well
    print(f"Running with DB Password: {vars['db_password']}")
    print(f"Running with Petfinder Payload: {vars['petfinder_payload']}")

    return vars



def setup_db():
    db_util = db_utils.db_utils(get_vars())

    # Run migrations to set up the DB
    db_util.execute_migration('teardown.sql')
    db_util.execute_migration('create_db.sql')
    # TODO maybe do some assertions to validate that the DB exists and has an expected structure?


    # Load petfinder metadata
    db_util.execute_queries(db_util.generate_metadata_queries())

    # Load actual petfinder animals
    db_util.execute_queries(db_util.generate_animal_queries(1))


setup_db()