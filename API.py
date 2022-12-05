import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from flask import Flask, jsonify
from core.database import *
import flask

app = Flask (__name__)

@app.route("/")
def index():
    return "Home page"

@app.route("/usercount", methods=["GET"])
def GetUserCount():
    connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        rowarray_list = []
        for row in rows:
            t = (row[0])
            rowarray_list.append(t)

        count = len(rowarray_list)
        j = {"usercount" : count}
        j = json.dumps(j)
        return flask.Response(j, mimetype="application/json")

@app.route("/servercount", methods=["GET"])
def GetServerCount():
    connection = ConnectionPool("postgresql://{}:{}@{}:{}/{}".format(database_username, database_password, database_ip, database_port, database_name))
    with connection.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servers")
        rows = cursor.fetchall()

        rowarray_list = []
        for row in rows:
            t = (row[0])
            rowarray_list.append(t)

        count = len(rowarray_list)
        j = {"servercount" : count}
        j = json.dumps(j)
        return flask.Response(j, mimetype="application/json")

if __name__ == "__main__":
    print("API online.")
    app.run(debug=True )