import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from psycopg.rows import dict_row
from flask import Flask, jsonify
from core.database import *
import flask

app = Flask (__name__)

@app.route("/")
def index():
    return "Home page"

@app.route("/usercount", methods=["GET"])
def GetUserCount():
    with db_connection.connection() as conn:
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
    with db_connection.connection() as conn:
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

@app.route("/inventory/<user_id>", methods=["GET"])
async def GetInventory(user_id):
    try:
        user = await getUser(user_id)
        resp = {"status": 200, "statusText": "success", "inventory": user["inventory"]["inventory"]}
        return flask.Response(json.dumps(resp), mimetype="application/json")
    except:
        resp = {"status": 404, "statusText": "user does not exist"}
        return flask.Response(json.dumps(resp), mimetype="application/json")

if __name__ == "__main__":
    print("API online.")
    app.run(debug=True)