import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from urllib.parse import quote_plus
from configparser import ConfigParser

db_config = ConfigParser()
db_config.read(os.path.join(BASE_DIR, "setting.conf"))
print(db_config.sections())
section_name = "pgsql"
db_name = db_config.get(section_name, "DB_NAME")
db_user = db_config.get(section_name, "USER")
db_pwd = db_config.get(section_name, "PWD")
db_host = db_config.get(section_name, "HOST")
db_port = db_config.get(section_name, "PORT")
table_name = "gb_industry"
def export_table(table_name):
    os.system(f"sqlacodegen --table {table_name} postgresql://{db_user}:{quote_plus(db_pwd)}@{db_host}:{db_port}/{db_name} > {table_name}.py")
export_table(table_name)