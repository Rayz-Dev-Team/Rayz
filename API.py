from quart import Quart, request
import quart
import os
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from tools.db_funcs import getAllUsers
from psycopg.rows import dict_row
from core.database import *
from functools import wraps
import requests

app = Quart(__name__)

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        userID = request.headers.get('UserID')
        token = request.headers.get('Authorization')

        if not userID:
            return {'message': 'UserID is missing'}, 401

        if not token:
            return {'message': 'Token is missing'}, 401
        
        users = await getAllUsers()
        user_list = []
        for i in users:
            user_list.append(i["id"])
        with db_connection.connection() as conn:
            if userID in user_list:
                if token == "1233":
                    return await f(*args, **kwargs)
                else:
                    return {'message': 'Token is invalid.'}, 401
            else:
                return {'message': 'UserID does not exist.'}, 401
    return decorated
    

@app.route('/')
async def index():
    return 'Turn back while you still can.'

@app.route("/<server_id>/staff", methods=["GET"])
async def GetStaffMembers(server_id):
    staff_member_id_list = {}
    req_roles = requests.get("https://www.guilded.gg/api/teams/{}/info".format(server_id))
    resp_roles = req_roles.json()
    mod_role_id_list = []
    for key, i in resp_roles["team"]["rolesById"].items():
        kick_ban_hex = 32
        if "general" in i["permissions"]:
            num_to_convert = i["permissions"]["general"]
            converted_num = num_to_convert & 32
            if converted_num == kick_ban_hex:
                mod_role_id_list.append(i["id"])

    req_server = requests.get("https://www.guilded.gg/api/teams/{}/members".format(server_id))
    resp_server = req_server.json()
    for i in resp_server["members"]:
        if "roleIds" in i:
            roles = i["roleIds"]
            for a in mod_role_id_list:
                if a in roles:
                    if i["id"] not in staff_member_id_list:
                        if "profilePicture" not in i:
                            i["profilePicture"] = "https://imgur.com/RGYNw2v"
                        staff_member_id_list[i["id"]] = {
                            "avatar": '{}'.format(i["profilePicture"]),
                            "name": '{}'.format(i["name"]),
                            "id": '{}'.format(i["id"])
                        }
    j = json.dumps(staff_member_id_list)
    return quart.Response(j, mimetype="application/json")


@app.route("/usercount", methods=["GET"])
@token_required
async def GetUserCount():
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
        return quart.Response(j, mimetype="application/json")

@app.route("/servercount", methods=["GET"])
@token_required
async def GetServerCount():
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
        return quart.Response(j, mimetype="application/json")

@app.route("/inventory/<user_id>", methods=["GET"])
@token_required
async def GetInventory(user_id):
    try:
        user = await getUser(user_id)
        resp = {"status": 200, "statusText": "success", "inventory": user["inventory"]["inventory"]}
        return quart.Response(json.dumps(resp), mimetype="application/json")
    except:
        resp = {"status": 404, "statusText": "user does not exist"}
        return quart.Response(json.dumps(resp), mimetype="application/json")

if __name__ == '__main__':
    host = os.environ['QUART_APP'] = '0.0.0.0'
    port = os.environ.get('QUART_RUN_PORT', '7777')
    app.run(host, port=int(port))