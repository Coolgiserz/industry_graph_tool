import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from configparser import ConfigParser
config_parser = ConfigParser()
config_parser.read(os.path.join(BASE_DIR, "setting.conf"))
pgsql_section = "pgsql"

db_name = config_parser.get(pgsql_section, "DB_NAME")
db_user = config_parser.get(pgsql_section, "USER")
db_pwd = config_parser.get(pgsql_section, "PWD")
db_host = config_parser.get(pgsql_section, "HOST")
db_port = config_parser.get(pgsql_section, "PORT")

redis_section = "redis"
redis_host = config_parser.get(redis_section, "HOST")
redis_port = config_parser.get(redis_section, "PORT")
redis_db = config_parser.get(redis_section, "DB")

neo4j_section = "neo4j"
neo4j_pwd = config_parser.get(neo4j_section, "PWD")
neo4j_db = config_parser.get(neo4j_section, "USER")
neo4j_uri = config_parser.get(neo4j_section, "URI")
def get_connect_string(dbname=None):
    if dbname is None:
        dbname = db_name
    return f"postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{dbname}"

print(get_connect_string(db_name))