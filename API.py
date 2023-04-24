from quart import Quart, request, send_file, Response, jsonify, url_for, redirect, abort, render_template
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
import secrets
import string
import time

with open('config/config.json') as f:
    config = json.load(f)

token = config["Token"]
cert = config["ssl_certificate"]
key = config["ssl_key"]


app = Quart(__name__, template_folder='api')
app = cors(app, allow_origin=["*"], allow_headers="*")

accepted_pull_tags_from_team = ["id", "name", "ownerId", "profilePicture", "memberCount", "socialInfo", "homeBannerImageLg"]
accepted_pull_tags_from_serverDB = ["id", "custom_blocked_words", "logs_channel_id", "server_prefix", "partner_status", "economy_multiplier", "moderation_module", "fun_module", "economy_module", "welcome_message", "welcome_channel", "log_traffic", "log_actions"]
accepted_pull_tags_from_userDB = ["id", "bank", "bank_secure", "pocket", "inventory", "commands_used", "cooldowns"]

async def _check_tokens(author):
	try:
		user = await getUser(author)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			if user["tokens"] == None or user["tokens"] == {}:
				new_account = {
					"tokens": {}
				}
				infoJson = json.dumps(new_account)
				cursor = conn.cursor()
				cursor.execute(f"UPDATE users SET tokens = %s WHERE ID = '{author}'",  [infoJson])
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def check_token(id, token):
    user = await getUser(id)
    takeaway = False
    if user == None:
        return False
    for i in user["tokens"]["tokens"]:
        if i == token:
            if user["tokens"]["tokens"][i]["token_active"] == True:
                takeaway = True
    return takeaway

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        userID = request.headers.get('UserID')
        token = request.headers.get('Authorization')

        if not userID:
            data = {"code": 401, "message": "UserID is missing."} 
            return jsonify(data)

        if not token:
            data = {"code": 401, "message": "Token is missing."} 
            return jsonify(data)
        
        users = await getAllUsers()
        user_list = []
        for i in users:
            user_list.append(i["id"])
        with db_connection.connection() as conn:
            if userID in user_list:
                check = await check_token(userID, token)
                if check == True:
                    return await f(*args, **kwargs)
                else:
                    data = {"code": 401, "message": "Token is invalid."} 
                    return jsonify(data)
            else:
                data = {"code": 401, "message": "UserID does not exist."} 
                return jsonify(data)
    return decorated

async def CheckServerValid_FromAPI(id: str):
    req_serverinfo = requests.get("https://www.guilded.gg/api/teams/{}/info".format(id))
    resp_serverinfo = req_serverinfo.json()
    valid = True
    if "code" in resp_serverinfo and "message" in resp_serverinfo:
        valid = {
            "code" : 404,
            "message" : "Server is private, or doesn't exist."
        }
    else:
        return valid

async def CheckUserValid_FromDB(id: str):
    users = await getAllUsers()
    user_list = []
    for i in users:
        user_list.append(i["id"])
    if id in user_list:
        valid = True
    else:
        valid = False
    return valid

async def CheckServerValid_FromDB(id: str):
    req_servers = await getAllServers()
    valid = False
    for i in req_servers:
        if id == i["id"]:
            valid = True
    return valid

async def CheckBotInServer(id: str):
    bot_in_server = False
    valid = await CheckServerValid_FromAPI(id)
    if valid == True:
        req_server = requests.get("https://www.guilded.gg/api/teams/{}/members".format(id))
        resp_server = req_server.json()
        for i in resp_server["members"]:
            if i["id"] == "m6oLkqLA":
                bot_in_server = True
    return bot_in_server

@app.errorhandler(404)
async def not_found(_):
    page_url = request.path
    return {'message': f'Page {page_url} does not exist.'}, 401

@app.route('/', methods=["GET"])
@route_cors(allow_origin="*")
async def index():
    return await render_template('index.html')

@app.route('/dashboard', methods=["GET"])
@route_cors(allow_origin="*")
async def dashboard():
    return await render_template('server.html')

@app.route('/dashboard/css/<file_name>.css', methods=["GET"])
@route_cors(allow_origin="*")
async def dashboard_css(file_name: str):
    return await send_file("dashboard/{}.css".format(file_name))

@app.route('/dashboard/js/<file_name>.js', methods=["GET"])
@route_cors(allow_origin="*")
async def dashboard_js(file_name: str):
    return await send_file("dashboard/{}.js".format(file_name))

@app.route("/image/logo.png", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"])
async def logo():
    return await send_file("assets/images/logo.png", mimetype="image")

@app.route('/server/<server_id>/channel/<channel_id>', methods=['GET'])
@token_required
async def ValidateChannel(server_id: str, channel_id: str):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        data = {"code": 404, "message": "Server doesn't exist in the database."} 
        return jsonify(data)
    if not valid_check == True:
        return jsonify(valid_check)
    if bot_in_server == False:
        data = {"code": 404, "message": "The bot is not in the server."} 
        return jsonify(data)

    get_channel_url = "https://www.guilded.gg/api/v1/channels/{}".format(channel_id)
    channel_url_headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(get_channel_url, headers=channel_url_headers)
    data = response.json()

    if "channel" in data:
        if not data["channel"]["type"] == "chat":
            data = {"code": 406, "message": "Channel type is not chat"} 
            return jsonify(data)

        data = {
            "code": 200,
            "message" : "Channel is valid",
            "channel" : {
                "id": data["channel"]["id"],
                "name": data["channel"]["name"],
            }
        }
        return jsonify(data)
    else:
        data = {"code": 404, "message": "Channel not found"}
        return jsonify(data)

@app.route('/token/<user_id>/validate', methods=['POST'])
@route_cors(allow_headers=["content-type"], allow_methods=["POST"], allow_origin="*")
async def ValidateToken(user_id: str):
    try:
        data = await request.json
        if "token" in data:
            token = data["token"]
            user_status = await CheckUserValid_FromDB(user_id)
            if user_status == True:
                user = await getUser(user_id)
                if token in user["tokens"]["tokens"]:
                    if user["tokens"]["tokens"][token]["token_active"] == False:
                        data = {"code": 401, "message": "Token is not active.", "status": False} 
                        return jsonify(data)
                    else:
                        data = {"code": 200, "message": "Token is active!", "status": True} 
                        return jsonify(data)
                else:
                    data = {"code": 401, "message": "Token doesn't exist.", "status": False} 
                    return jsonify(data)
            else:
                data = {"code": 404, "message": "Invalid user ID."} 
                return jsonify(data)
        else:
            data = {"code": 404, "message": "Token param not found."} 
            return jsonify(data)
    except:
        data = {"code": 500, "message": "Bad request."} 
        return jsonify(data)
        

@app.route("/404")
@route_cors(allow_headers=["content-type"], allow_origin="*")
async def NotFound():
    with open("images/404.png", "rb") as f:
        image_data = f.read()
    response = quart.Response(image_data, mimetype="image/png")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/token/<user_id>/generate", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GenerateToken(user_id: str):
    DB_check = await CheckUserValid_FromDB(user_id)
    if DB_check == True:
        await _check_tokens(user_id)
        curr_time = time.time()
        user = await getUser(user_id)
        token = str(secrets.token_hex(32))
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))
        with db_connection.connection() as conn:
            user["tokens"]["tokens"][token] = {
                "token_active": False,
                "password": "{}".format(password),
                "last_use": curr_time
            }
            updated_tokens = user["tokens"]
            infoJson = simplejson.dumps(updated_tokens)
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET tokens = %s WHERE ID = '{user_id}'",  [infoJson])
            conn.commit()
            data = {"code": 200, "message": "Token generated.", "token": token, "password": password} 
            return jsonify(data)
    else:
        data = {"code": 404, "message": "That user ID doesn't exist."} 
        return jsonify(data)

@app.route("/server/<server_id>/bot-permissions", methods=["GET"])
@token_required
async def GetBotPermissions(server_id: str):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        data = {"code": 404, "message": "Server doesn't exist in the database."} 
        return jsonify(data)
    if not valid_check == True:
        data = valid_check
        return jsonify(data)
    if bot_in_server == False:
        data = {"code": 404, "message": "The bot is not in the server."} 
        return jsonify(data)

    req_serverinfo = requests.get("https://www.guilded.gg/api/teams/{}/info".format(server_id))
    resp_serverinfo = req_serverinfo.json()

    permissions = {
        "kick_perms": False,
        "manage_roles_perms": False,
        "manage_channels_perms": False,
        "moderator_view_perms": False,
        "manage_messages_perms": False,
        "manage_xp_perms": False
    }
    
    #Get permissions
    for key, i in resp_serverinfo["team"]["rolesById"].items():
        kick_ban_hex = 32
        manage_roles_perms_hex = 16384
        manage_channels_perms_hex = 1024
        moderator_view_perms_hex = 32768
        manage_messages_perms_hex = 4
        manage_xp_perms_hex = 1

        if "general" in i["permissions"]:
            num_to_convert = i["permissions"]["general"]
            kick_perms = num_to_convert & kick_ban_hex
            manage_roles_perms = num_to_convert & manage_roles_perms_hex
            manage_channels_perms = num_to_convert & manage_channels_perms_hex
            moderator_view_perms = num_to_convert & moderator_view_perms_hex
            if kick_perms == kick_ban_hex:
                permissions["kick_perms"] = True
            if manage_roles_perms == manage_roles_perms_hex:
                permissions["manage_roles_perms"] = True
            if manage_channels_perms == manage_channels_perms_hex:
                permissions["manage_channels_perms"] = True
            if moderator_view_perms == moderator_view_perms_hex:
                permissions["moderator_view_perms"] = True

        if "chat" in i["permissions"]:
            num_to_convert = i["permissions"]["chat"]
            manage_messages_perms = num_to_convert & manage_messages_perms_hex
            if manage_messages_perms == manage_messages_perms_hex:
                permissions["manage_messages_perms"] = True

        if "xp" in i["permissions"]:
            num_to_convert = i["permissions"]["xp"]
            manage_xp_perms = num_to_convert & manage_xp_perms_hex
            if manage_xp_perms == manage_xp_perms_hex:
                permissions["manage_xp_perms"] = True
                
    data = {"code": 200, "message": "Here is Rayz's permissions", "permissions": permissions} 
    return jsonify(data)

@app.route("/server/<server_id>/settings", methods=["GET"])
@token_required
async def GetServerSettings(server_id: str):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        data = {"code": 404, "message": "Server doesn't exist in the database."} 
        return jsonify(data)
    if not valid_check == True:
        data = valid_check
        return jsonify(data)
    if bot_in_server == False:
        data = {"code": 404, "message": "The bot is not in the server."} 
        return jsonify(data)
    
    main_output = {}
    output_server_data = {}

    server_data = await getServer(server_id)
    for i in accepted_pull_tags_from_serverDB:
        try:
            output_server_data[i] = server_data[i]
        except:
            pass

    data = {"code": 200, "message": "Here is Rayz's settings for the server.", "rayz_settings": output_server_data} 
    return jsonify(data)


@app.route("/server/<server_id>/info", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetServerInfo(server_id: str):
    DB_check = await CheckServerValid_FromDB(server_id)
    valid_check = await CheckServerValid_FromAPI(server_id)
    bot_in_server = await CheckBotInServer(server_id)
    if DB_check == False:
        data = {"code": 404, "message": "Server doesn't exist in the database."} 
        return jsonify(data)
    if not valid_check == True:
        data = valid_check
        return jsonify(data)
    if bot_in_server == False:
        data = {"code": 404, "message": "The bot is not in the server."} 
        return jsonify(data)
    main_output = {}
    output_server_json = {}
    output_server_data = {}
    output_rayz_settings_json = {}
    bots_list = {}
    staff_member_id_list = {}
    mod_role_id_list = []

    #GET SERVER INFO ------------------------------------------------------
    req_serverinfo = requests.get("https://www.guilded.gg/api/teams/{}/info".format(server_id))
    resp_serverinfo = req_serverinfo.json()

    req_server = requests.get("https://www.guilded.gg/api/teams/{}/members".format(server_id))
    resp_server = req_server.json()
    #-----------------------------------------------------------------------

    for i in accepted_pull_tags_from_team:
        try:
            output_server_json[i] = resp_serverinfo["team"][i]
        except:
            pass
    
    server_data = await getServer(server_id)
    for i in accepted_pull_tags_from_serverDB:
        try:
            output_server_data[i] = server_data[i]
        except:
            pass

    #GET SERVER MEMBERS ------------------------------------------------------
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
    #-----------------------------------------------------------------------
    
    #GET STAFF MEMBERS ------------------------------------------------------
    for key, i in resp_serverinfo["team"]["rolesById"].items():
        kick_ban_hex = 32
        if "general" in i["permissions"]:
            num_to_convert = i["permissions"]["general"]
            converted_num = num_to_convert & 32
            if converted_num == kick_ban_hex:
                mod_role_id_list.append(i["id"])

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
    #-----------------------------------------------------------------------

    main_output["server_data"] = output_server_json
    main_output["rayz_settings"] = output_server_data
    main_output["server_staff"] = staff_member_id_list
    main_output["bots_list"] = bots_list

    data = {"code": 200, "message": ":D", "server_data": output_server_json, "server_staff": staff_member_id_list}
    return jsonify(data)

@app.route("/user/<user_id>/info", methods=["GET"])
@route_cors(allow_headers=["content-type"], allow_methods=["GET"], allow_origin="*")
async def GetUserInfo(user_id: str):
    user_data_output = {}
    user_data = await getUser(user_id)
    if user_data == None:
        data = {"code": 404, "message": "User doesn't exist in the database."}
        return jsonify(data)
        
    else:
        for i in accepted_pull_tags_from_userDB:
            try:
                user_data_output[i] = user_data[i]
            except:
                pass
        data = {"code": 200, "message": "Here is the data for the user.", "user_data": user_data_output}
        return jsonify(data)

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
    data = {"code": 200, "message": "Here is every GG member.", "GG": profiles_list}
    return jsonify(data)

@app.route("/stats", methods=["GET"])
#@token_required
async def GetServerCount():
    req_server = requests.get("https://www.guilded.gg/api/users/m6oLkqLA/teams")
    resp_server = req_server.json()
    user_count = 0
    server_count = len(resp_server["teams"])
    
    for i in resp_server["teams"]:
        user_count += i["memberCount"]


    data = {"code": 200, "message": "Stats.", "servers": server_count, "users": user_count}
    return jsonify(data)

@app.route("/inventory/<user_id>", methods=["GET"])
@token_required
async def GetInventory(user_id: str):
    try:
        user = await getUser(user_id)
        data = {"code": 200, "message": "success", "inventory": user["inventory"]["inventory"]}
        return jsonify(data)
    except:
        data = {"code": 404, "message": "User does not exist."}
        return jsonify(data)

if __name__ == '__main__':
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(cert, key)
    config = Config()
    config.bind = ['localhost:7777']
    config.ssl = context
    asyncio.run(serve(app, config))