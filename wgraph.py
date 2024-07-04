"""
Functions to download data to analyze using the wf market API.
Saves data as a file.
"""

import os
import json
import time
import requests

def getitems(tag):
    """Get current item list."""

    items = []
    for filename in os.listdir("./items/wfm-items/tracked/items/"):
        with open(os.path.join("./items/wfm-items/tracked/items/"\
                               ,filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "tags" in data and tag == "arcanes":
                if "arcane_enhancement" in data["tags"]:
                    make_url = url_gen(data)
                    items.append(make_url)
                    #items.append(data.get('i18n', {}).get('en', {}).get('item_name'))
            if "tags" in data and tag == "mods":
                if "mod" in data["tags"] and "warframe" in data["tags"]:
                    make_url = url_gen(data)
                    items.append(make_url)
    return items

def url_gen(data):
    """Generates url for the API request."""

    pair = []
    name = data.get('url_name', {})
    filename = os.path.join("./dump/",str(data.get('i18n', {}).get('en', {})\
                                          .get('item_name')) + ".json")
    pair.append(filename)
    entire_url = "https://api.warframe.market/v1/items/"\
         + str(name) + "/statistics"
    pair.append(entire_url)
    return pair

def fetch_json_and_save(url):
    """Fetches json data and saves it as a file."""

    try:
        response = requests.get(url[1], timeout=50)
        response.raise_for_status()  # Check for HTTP errors
        json_data = response.json()  # Parse the JSON data from the response
        with open(url[0], 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the JSON data: {e}")
    except Exception as e:
        print(f"An error occurred while saving the JSON data: {e}")

lista = getitems("mods") # "arcanes", "mods", "component", "weapon", "prime", "relic"
for urls in lista:
    fetch_json_and_save(urls)
    time.sleep(3)
    print(f"Processing {urls[0]}")
