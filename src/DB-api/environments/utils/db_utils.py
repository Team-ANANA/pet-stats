import mysql.connector
from pathlib import Path
import petfinder_utils
from pypika import Table, MySQLQuery, terms
import dateutil.parser


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
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()
        migration_path = Path(__file__).parent.parent / "migrations" / f"{migration}"
        fd = open(migration_path, "r")
        migration_file = fd.read()
        fd.close()
        migration_operations = migration_file.replace("\n", "").split(";")

        # execute migration operations
        for operation in migration_operations:
            cursor.execute(operation)

        cnx.commit()

    def generate_metadata_queries(self):
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

    def generate_animal_queries(self, page_max):
        res = self.petfinder_utils.get_petfinder_data(
            "/v2/animals", self.petfinder_utils.get_access_token()
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

        while res.get("pagination").get("current_page") <= page_max:
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
            # go to next page
            res = self.petfinder_utils.get_petfinder_data(
                res["pagination"]["_links"]["next"]["href"],
                self.petfinder_utils.get_access_token(),
            )
        return ret

    def execute_queries(self, queries):
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()
        for query in queries:
            cursor.execute(query.get_sql())
        cnx.commit()
