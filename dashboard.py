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


app = Quart(__name__, template_folder='dashboard')
app = cors(app, allow_origin=["*"], allow_headers="*")

@app.errorhandler(404)
async def not_found(_):
    page_url = request.path
    return {'message': f'Page {page_url} does not exist.'}, 401

@app.route('/', methods=["GET"])
@route_cors(allow_origin="*")
async def index():
    return await render_template('index.html')

@app.route('/gilgang', methods=["GET"])
@route_cors(allow_origin="*")
async def gilgang():
    return await render_template('gilgang.html')

@app.route('/dashboard', methods=["GET"])
@route_cors(allow_origin="*")
async def dashboard():
    return await render_template('server.html')

@app.route('/dashboard/<server_id>', methods=["GET"])
@route_cors(allow_origin="*")
async def dashboard_staff(server_id):
    return await render_template('staff.html')

if __name__ == '__main__':
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(cert, key)
    config = Config()
    config.bind = ['localhost:7774']
    config.ssl = context
    asyncio.run(serve(app, config))