import mysql.connector
from pathlib import Path
import petfinder_utils
from pypika import Table, MySQLQuery, terms
import dateutil.parser
import time
import logging
class db_utils:
    def __init__(self, env):
        self.db_config = {
            "user": "root",
            "password": env.get("db_password"),
            "port": "3306",
            "host": "localhost",
            "database": "pet-stats",
        }
        self.petfinder_utils = petfinder_utils.petfinder_utils(env)

    def execute_migration(self, migration):
        # execute sql migration from file in migrations folder
        logging.info('Attempting to connect to SQL server')
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()
        migration_path = Path(__file__).parent.parent / "migrations" / f"{migration}"
        logging.info(f"Running migration: {migration}, located at {migration_path}")
        fd = open(migration_path, "r")
        migration_file = fd.read()
        fd.close()
        migration_operations = migration_file.replace("\n", "").split(";")

        # execute migration operations
        for operation in migration_operations:
            logging.debug(F"Executing migration operation: {operation}")
            cursor.execute(operation)

        cnx.commit()

    def generate_metadata_queries(self):
        # load metadata queries from petfinder API to insert into DB
        logging.info("Attempting to generate metadata insert statements")
        res = self.petfinder_utils.get_petfinder_data(
            "/v2/types", self.petfinder_utils.get_access_token()
        )
        ret = []
        types = Table("type")
        metadata = {
            "coats": Table("coat"),
            "colors": Table("color"),
            "genders": Table("gender"),
        }
        for type in res.get("types"):
            # add type to types table
            ret.append(MySQLQuery.into(types).columns("name").insert(type.get("name")))
            # add other metadata
            for name, table in metadata.items():
                for descriptor in type.get(name):
                    ret.append(
                        MySQLQuery.into(table)
                        .columns("type_id", "descriptor")
                        .insert(
                            MySQLQuery.from_(types)
                            .select(types.id)
                            .where(types.name == type.get("name")),
                            descriptor,
                        )
                    )
            # add breed metadata
            breed_link = type.get("_links").get("breeds").get("href")
            breed_res = self.petfinder_utils.get_petfinder_data(
                breed_link, self.petfinder_utils.get_access_token()
            )
            breeds = Table("breed")
            for breed in breed_res.get("breeds"):
                ret.append(
                    MySQLQuery.into(breeds)
                    .columns("type_id", "descriptor")
                    .insert(
                        MySQLQuery.from_(types)
                        .select(types.id)
                        .where(types.name == type.get("name")),
                        breed.get("name"),
                    )
                )
        return ret

    def generate_animal_queries(self, page_start, page_end):
        logging.info(f"Loading animal data, from page {page_start} to page {page_end}")
        # generate a list of INSERT statements for a given page range
        # for the /animals route in petfinder
        res = self.petfinder_utils.get_petfinder_data(
            f"/v2/animals?page={page_start}&limit=100", self.petfinder_utils.get_access_token()
        )
        ret = []
        animals = Table("animals")
        types = Table("type")
        coats = Table("coat")
        colors = Table("color")
        genders = Table("gender")
        breeds = Table("breed")

        ages = Table("age")
        sizes = Table("size")
        status = Table("status")
        countries = Table("country")
        states = Table("state")

        while res.get("pagination").get("current_page") <= page_end:
            for animal in res.get("animals"):
                if animal["contact"]["address"]["country"] in ["CA", "US"]:
                    query = (
                        MySQLQuery.into(animals)
                        .insert(
                            animal["id"],
                            animal["organization_id"],
                            MySQLQuery.from_(types)
                            .select(types.id)
                            .where(types.name == animal["type"]),
                            animal["species"],
                            # breeds
                            # primary breed
                            MySQLQuery.from_(breeds)
                            .select(breeds.id)
                            .where(
                                breeds.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(breeds.descriptor == animal["breeds"]["primary"]),
                            # secondary breed
                            MySQLQuery.from_(breeds)
                            .select(breeds.id)
                            .where(
                                breeds.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(breeds.descriptor == animal["breeds"]["secondary"]),
                            animal["breeds"]["mixed"],
                            animal["breeds"]["unknown"],
                            # colors
                            # primary color
                            MySQLQuery.from_(colors)
                            .select(colors.id)
                            .where(
                                colors.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(colors.descriptor == animal["colors"]["primary"]),
                            # secondary color
                            MySQLQuery.from_(colors)
                            .select(colors.id)
                            .where(
                                colors.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(colors.descriptor == animal["colors"]["secondary"]),
                            # tertiary color
                            MySQLQuery.from_(colors)
                            .select(colors.id)
                            .where(
                                colors.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(colors.descriptor == animal["colors"]["tertiary"]),
                            # age
                            MySQLQuery.from_(ages)
                            .select(ages.id)
                            .where(ages.descriptor == (animal["age"])),
                            # gender
                            MySQLQuery.from_(genders)
                            .select(genders.id)
                            .where(
                                genders.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(genders.descriptor == animal["gender"]),
                            # size
                            MySQLQuery.from_(sizes)
                            .select(sizes.id)
                            .where(sizes.descriptor == (animal["size"])),
                            # coat
                            MySQLQuery.from_(coats)
                            .select(coats.id)
                            .where(
                                coats.type_id
                                == (
                                    MySQLQuery.from_(types)
                                    .select(types.id)
                                    .where(types.name == animal["type"])
                                )
                            )
                            .where(coats.descriptor == animal["gender"]),
                            # attributes
                            animal["attributes"]["spayed_neutered"],
                            animal["attributes"]["house_trained"],
                            animal["attributes"]["declawed"],
                            animal["attributes"]["special_needs"],
                            animal["attributes"]["shots_current"],
                            # environment
                            animal["environment"]["children"],
                            animal["environment"]["dogs"],
                            animal["environment"]["cats"],
                            # description/name
                            animal["name"],
                            animal["description"],
                            # status
                            MySQLQuery.from_(status)
                            .select(status.id)
                            .where(status.descriptor == (animal["status"])),
                            # date published at, in ISO8601 -> python date
                            dateutil.parser.isoparse(animal["published_at"]),
                            # country
                            MySQLQuery.from_(countries)
                            .select(countries.id)
                            .where(
                                countries.descriptor
                                == (animal["contact"]["address"]["country"])
                            ),
                            # state
                            MySQLQuery.from_(states)
                            .select(states.id)
                            .where(
                                states.descriptor
                                == animal["contact"]["address"]["state"]
                            ),
                        )
                        .on_duplicate_key_update(animals.id, terms.Values(animals.id))
                    )
                    ret.append(query)
                    logging.debug(f"Generated insert statement for animal: \n {query.get_sql()}")
            # go to next page
            res = self.petfinder_utils.get_petfinder_data(
                res["pagination"]["_links"]["next"]["href"] + '&limit=100',
                self.petfinder_utils.get_access_token()
            )
            logging.debug(f"Loading page {res.get('pagination').get('current_page')}")
        return ret

    def execute_queries(self, queries):
        cnx = mysql.connector.connect(**self.db_config)
        logging.info(f"Executing {len(queries)} queries")
        cursor = cnx.cursor()
        for query in queries:
            logging.debug(f"Executed query {query.get_sql()}")
            cursor.execute(query.get_sql())
        logging.info(f"Committed {len(queries)} queries.")
        cnx.commit()


    def load_large_animal_dataset(self, num_pages):
        # load num_pages animals, where each page holds 100 animals.
        logging.info(f"Loading {num_pages} pages of animals.")
        # this exists for 2 reasons:
        #  1. tp periodically dump loaded data into the DB to not overflow RAM
        #  2. to force request rate limiting in a very primitive manner (50 reqs/second)
        for page_start in range(1, num_pages, 10):
            page_end = min(page_start+10, num_pages)
            logging.info(f"Loading pages: {page_start} to {page_end}")
            self.execute_queries(self.generate_animal_queries(page_start, page_end))
            # rudimentary rate limiting
            logging.info('Sleeping to avoid rate limit')
            time.sleep(0.2)

        logging.info(f"Loaded {num_pages} pages of animals.")

