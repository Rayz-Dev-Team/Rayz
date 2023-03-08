from quart import Quart, request, send_file, Response, jsonify, url_for, redirect, abort, render_template_string
import quart
import os
import psycopg
import asyncio
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from tools.db_funcs import getAllUsers
from tools.db_funcs import getAllServers
from psycopg.rows import dict_row
from core.database import *
from functools import wraps
import requests
import ssl
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart_cors import cors, route_cors
import simplejson


app = Quart(__name__)
app = cors(app, allow_origin=["*"], allow_headers="*")

accepted_pull_tags_from_team = ["id", "name", "ownerId", "profilePicture", "memberCount", "socialInfo", "homeBannerImageLg"]


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

async def CheckServerValid_FromAPI(id):
    req_serverinfo = requests.get("https://www.guilded.gg/api/teams/{}/info".format(server_id))
    resp_serverinfo = req_serverinfo.json()
    valid = True
    if "code" in resp_serverinfo and "message" in resp_serverinfo:
        valid = {
            "code" : 404,
            "message" : "Server is private, or doesn't exist."
        }
    else:
        return valid

async def CheckServerValid_FromDB(id):
    req_servers = await GetAllServers()
    valid = False
    for i in req_servers:
        if id == i["id"]:
            valid = True
    return valid

async def CheckBotInServer(id):
    req_server = requests.get("https://www.guilded.gg/api/teams/{}/members".format(id))
    resp_server = req_server.json()
    bot_in_server = False
    for i in resp_server["members"]:
        if i["id"] == "m6oLkqLA":
            bot_in_server = True
    return bot_in_server

@app.errorhandler(404)
async def not_found(error):
    page_url = request.path
    return {'message': f'Page {page_url} does not exist.'}, 401

@app.route('/', methods=['GET'])
@route_cors(allow_origin="*")
async def index():
    return 'Example public endpoints are /stats, /server_id/staff, /server_id/bots'

@app.route("/capoo")
@route_cors(allow_headers=["content-type"], allow_origin="*")
async def Capoo():
    with open("packs/capoo/Capoo_squish.gif", "rb") as f:
        image_data = f.read()
    response = quart.Response(image_data, mimetype="image/gif")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/404")
@route_cors(allow_headers=["content-type"], allow_origin="*")
async def NotFound():
    with open("images/404.png", "rb") as f:
        image_data = f.read()
    response = quart.Response(image_data, mimetype="image/png")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/pack/<pack_name>", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetPack(pack_name):
    if pack_name == "capoo":
        image_url = url_for('Capoo', _external=True)

        capoo_pack = {
            "name": "Capoo Emoji Pack",
            "author": "Rayz API",
            "emotes": [
                {
                    "name": "capoo_cry",
                    "url": "https://api.rayzbot.xyz/capoo"
                }
            ]
        }
        response = quart.Response(json.dumps(capoo_pack), mimetype='application/json')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route("/<server_id>/info", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetServerInfo(server_id):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    if DB_check == False:
        error_response = {
            "code" : 404,
            "message" : "Server doesn't exist in the database."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if not valid_check == True:
        j = json.dumps(valid_check)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if bot_in_server == False:
        error_response = {
            "code" : 404,
            "message" : "The bot is not in the server."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    main_output = {}
    output_server_json = {}
    output_rayz_settings_json = {}
    req_serverinfo = requests.get("https://www.guilded.gg/api/teams/{}/info".format(server_id))
    resp_serverinfo = req_serverinfo.json()
    for i in accepted_pull_tags_from_team:
        try:
            output_server_json[i] = resp_serverinfo["team"][i]
        except:
            pass

    main_output["server_data"] = output_server_json
    main_output["rayz_settings"] = await getServer(server_id)

    j = simplejson.dumps(main_output)
    response = quart.Response(j, mimetype="application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/<server_id>/staff", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetStaffMembers(server_id):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        error_response = {
            "code" : 404,
            "message" : "Server doesn't exist in the database."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if not valid_check == True:
        j = json.dumps(valid_check)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if bot_in_server == False:
        error_response = {
            "code" : 404,
            "message" : "The bot is not in the server."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
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
                        if "profileBannerBlur" not in i:
                            i["profileBannerBlur"] = 404
                        if "type" not in i:
                            staff_member_id_list[i["id"]] = {
                                "avatar": '{}'.format(i["profilePicture"]),
                                "name": '{}'.format(i["name"]),
                                "id": '{}'.format(i["id"]),
                                "banner": '{}'.format(i["profileBannerBlur"])
                            }
    j = json.dumps(staff_member_id_list)
    response = quart.Response(j, mimetype="application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/<server_id>/bots", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetBots(server_id):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        error_response = {
            "code" : 404,
            "message" : "Server doesn't exist in the database."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if not valid_check == True:
        j = json.dumps(valid_check)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    if bot_in_server == False:
        error_response = {
            "code" : 404,
            "message" : "The bot is not in the server."
        }
        j = json.dumps(error_response)
        response = quart.Response(j, mimetype="application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    bots_list = {}
    req_server = requests.get("https://www.guilded.gg/api/teams/{}/members".format(server_id))
    resp_server = req_server.json()
    for i in resp_server["members"]:
        if "profilePicture" not in i:
            i["profilePicture"] = "https://imgur.com/RGYNw2v"

        if "profileBannerBlur" not in i:
            i["profileBannerBlur"] = "https://theme.zdassets.com/theme_assets/9580103/a66d540c984b3fd96c37e2fb8b327607cc1e836c.png"

        if "type" in i:
           bots_list[i["id"]] = {
                "avatar": '{}'.format(i["profilePicture"]),
                "name": '{}'.format(i["name"]),
                "id": '{}'.format(i["id"]),
                "banner": '{}'.format(i["profileBannerBlur"])
            }
    j = json.dumps(bots_list)
    response = quart.Response(j, mimetype="application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/gilgang", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetGGMembers():
    gg_members_list = []
    profiles_list = {}
    req_server = requests.get("https://www.guilded.gg/api/teams/VRzvL9bR/members")
    resp_server = req_server.json()
    for i in resp_server["members"]:

        if not "profilePicture" in i:
            i["profilePicture"] = "https://imgur.com/RGYNw2v"

        if "profileBannerBlur" not in i:
            i["profileBannerBlur"] = "https://theme.zdassets.com/theme_assets/9580103/a66d540c984b3fd96c37e2fb8b327607cc1e836c.png"

        if "type" not in i:
            profiles_list[i["id"]] = {
                "id": "{}".format(i["id"]),
                "avatar": "{}".format(i["profilePicture"]),
                "name": "{}".format(i["name"])
            }
    j = json.dumps(profiles_list)
    response = quart.Response(j, mimetype="application/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

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

@app.route("/stats", methods=["GET"])
#@token_required
async def GetServerCount():
    req_server = requests.get("https://www.guilded.gg/api/users/m6oLkqLA/teams")
    resp_server = req_server.json()
    user_count = 0
    server_count = len(resp_server["teams"])
    
    for i in resp_server["teams"]:
        user_count += i["memberCount"]

    j = {"servers" : server_count, "users" : user_count}
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
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('C:/Users/Administrator/Desktop/cert.pem', 'C:/Users/Administrator/Desktop/key.pem')
    config = Config()
    config.bind = ['localhost:7777']
    config.ssl = context
    asyncio.run(serve(app, config))
