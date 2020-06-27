import json
import requests
import re

url_base = "https://store.steampowered.com/api/appdetails?appids="
header = {'Content-Type': 'application/json'}

def get_game_info(steamid):
    url = url_base + str(steamid)
    response = requests.get(url, headers=header)

    data = json.loads(response.content.decode('utf-8'))

    if data is None or data[str(steamid)]['success'] != True:
        return None

    #Trims html characters
    description = data[str(steamid)]["data"]["short_description"]
    fixed_description = description.replace('&amp;', '&')

    #Solves error if game is free
    price = 0.00
    if data[str(steamid)]["data"]["is_free"] != True:
        #trim dollar sign
        price = float(data[str(steamid)]["data"]["price_overview"]["final_formatted"][1:])

    return {
        "name": data[str(steamid)]["data"]["name"],
        "description": fixed_description,
        "price": price
    }
