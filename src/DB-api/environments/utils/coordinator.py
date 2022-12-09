# script that runs the import and handles getting environment variables + making sure the Petfinder API is up
import os
import db_utils

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('db.log'), logging.StreamHandler()])

def get_vars():
    logging.info('Trying to get environment variables')
    vars = {
        "db_password": os.environ.get('PET_STATS_DB_PASSWORD'),
        "petfinder_payload": os.environ.get('PET_STATS_PETFINDER_PAYLOAD'),
    }
    if None in vars.values():
        logging.fatal('Unable to get environment variables, exit')
        exit()

    logging.info(f"Running with DB Password: {vars['db_password']}")
    logging.info(f"Running with Petfinder Payload: {vars['petfinder_payload']}")
    
    return vars



def setup_db():

    db_util = db_utils.db_utils(get_vars())

    # Run migrations to set up the DB
    logging.info('Attempting to run migrations to set up database')
    db_util.execute_migration('teardown.sql')
    db_util.execute_migration('create_db.sql')
    db_util.execute_migration('add_enums.sql')

    # Load petfinder metadata
    logging.info("Loading petfinder metadata")
    db_util.execute_queries(db_util.generate_metadata_queries())

    # Load actual petfinder animals
    logging.info("Loading animals")
    db_util.load_large_animal_dataset(7)

    logging.info("Loading successful, exiting.")

setup_db()