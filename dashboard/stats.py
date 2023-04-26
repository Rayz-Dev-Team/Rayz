import requests
import pyodide_http

pyodide_http.patch_all()

response = requests.get("https://api.rayzbot.xyz/stats")
response = response.json()
display("{} servers, {} users.".format(response["servers"], response["users"]), target="StatDisplay", append=False)