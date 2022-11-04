import json

with open('config/config.json') as f:
    config = json.load(f)

database_name = config["database_name"]
database_port = config["database_port"]
database_password = config["database_password"]
database_username = config["database_username"]
