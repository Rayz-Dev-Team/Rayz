import json
import psycopg
from psycopg_pool import ConnectionPool 

with open('config/config.json') as f:
    config = json.load(f)

database_name = config["database_name"]
database_port = config["database_port"]
database_password = config["database_password"]
database_username = config["database_username"]
database_ip = config["database_ip"]
api_token = config["api_token"]

db_connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))