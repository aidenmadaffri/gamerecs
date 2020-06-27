import json
import requests
import re

url_base = "https://store.steampowered.com/api/appdetails?appids="
header = {'Content-Type': 'application/json'}

def get_game_info(steamid):
    url = url_base + str(steamid)
    response = requests.get(url, headers=header)

    data = json.loads(response.content.decode('utf-8'))

    if data[str(steamid)]['success'] == "True":
        return None

    description = data[str(steamid)]["data"]["short_description"]
    fixed_description = description.replace('&amp;', '&')

    return {
        "name": data[str(steamid)]["data"]["name"],
        "description": fixed_description,
        "price": data[str(steamid)]["data"]["price_overview"]["final_formatted"]
    }
