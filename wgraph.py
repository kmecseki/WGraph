"""
Functions to download data to analyze using the wf market API.
Saves data as a file.
"""

import os
import json
import time
from datetime import date, datetime
import requests

def getitems(*args, no=None):
    """Get current item list."""

    items = []
    for arg in args:
        if arg=="Suda" or arg=="Hexis":
            with open(arg + ".txt",'r') as f:
                for line in f:
                    pair = []
                    item_name = line.strip('\n')
                    file_name = os.path.join("./dump/",str(item_name) + ".json")
                    pair.append(file_name)
                    item_lower = item_name.replace(" ", "_").lower()
                    entire_url = "https://api.warframe.market/v1/items/"\
                        + str(item_lower) + "/statistics"
                    pair.append(entire_url)
                    items.append(pair)
            return items

    for filename in os.listdir("./items/wfm-items/tracked/items/"):
        with open(os.path.join("./items/wfm-items/tracked/items/"\
                               ,filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "tags" in data:
                if all(arg in data["tags"] for arg in args):# and no is not None and no not in data["tags"]:
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
    """Fetches json data and saves it as a file if the file is not recent (older than a week or doesn't exist)."""
    
    try:
        with open(url[0], 'r', encoding='utf-8') as file:
            data = json.load(file)
            file_date = datetime.strptime(data["payload"]["statistics_live"]["48hours"][0]["datetime"][0:10], "%Y-%m-%d").date()
            today = date.today()
            age = (today-file_date).days
            if age <= 3:
                return
    except FileNotFoundError:
        pass

    try:
        time.sleep(1) # Make sure we don't exceed time between requests
        response = requests.get(url[1], timeout=50)
        response.raise_for_status()  # Check for HTTP errors
        json_data = response.json()  # Parse the JSON data from the response
        with open(url[0], 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the JSON data: {e}")
    except Exception as e:
        print(f"An error occurred while saving the JSON data: {e}")

def download_and_save(lista):
    i = 1
    N = len(lista)
    for urls in lista:
        fetch_json_and_save(urls)
        print(f"Processing {urls[0]}, {i}/{N}")
        i += 1

