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
        # Get Syndicate items
        if arg=="Suda" or arg=="Hexis" or arg=="Loka" or arg=="Steel" or arg=="Perrin" or arg=="Red":
            with open(arg + ".txt",'r') as f:
                for line in f:
                    item_name = line.strip('\n')
                    pair = make_pair(item_name)
                    items.append(pair)
            return items

    for filename in os.listdir("./items/wfm-items/tracked/items/"):
        with open(os.path.join("./items/wfm-items/tracked/items/"\
                               ,filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "tags" in data:
                if no == None:
                    if all(arg in data["tags"] for arg in args):
                        make_url = url_gen_from_json(data)
                        items.append(make_url)
                else:
                    if all(arg in data["tags"] for arg in args) and all(arg not in data["tags"] for arg in no):
                        #if all(arg in data["tags"] for arg in args):# and no is not None and no not in data["tags"]:
                        make_url = url_gen_from_json(data)
                        items.append(make_url)
    return items

def make_pair(item_name):
    '''From item name to a pair of filename in dump and a link'''

    pair = []
    file_name = os.path.join("./dump/items/",str(item_name) + ".json")
    pair.append(file_name)
    url = gen_wfapi_url(item_name)
    pair.append(url)
    return pair

def gen_wfapi_url(item_name):
    item_lower = item_name.replace(" ", "_").lower()
    entire_url = "https://api.warframe.market/v1/items/" + str(item_lower) + "/statistics"
    return entire_url

def url_gen_from_json(data):
    """Generates url from the json file for the API request."""

    pair = []
    name = data.get('url_name', {})
    filename = os.path.join("./dump/items/", str(data.get('i18n', {}).get('en', {})\
                                          .get('item_name')) + ".json")
    pair.append(filename)
    entire_url = "https://api.warframe.market/v1/items/"\
         + str(name) + "/statistics"
    pair.append(entire_url)
    return pair

def fetch_json_and_save(pair):
    """Fetches json data and saves it as a file if the file is not recent (older than a week or doesn't exist)."""
    
    try:
        with open(pair[0], 'r', encoding='utf-8') as file:
            data = json.load(file)
            file_date = datetime.strptime(data["payload"]["statistics_live"]["48hours"][0]["datetime"][0:10], "%Y-%m-%d").date()
            today = date.today()
            age = (today-file_date).days
            if age <= 3:
                return
    except FileNotFoundError:
        pass
    download_json(pair[1], pair[0])

def download_json(url, file_name):
    try:
        time.sleep(1) # Make sure we don't exceed time between requests
        response = requests.get(url, timeout=50)
        response.raise_for_status()  # Check for HTTP errors
        json_data = response.json()  # Parse the JSON data from the response
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the JSON data: {e}")
    except Exception as e:
        print(f"An error occurred while saving the JSON data: {e}")

def download_and_save(lista):

    N = len(lista)
    for ind, urls in enumerate(lista):
        fetch_json_and_save(urls)
        print(f"Processing {urls[0]}, {ind}/{N}")

#def get_user_orders(filename):

def get_current_orders(username, bool_refresh=False):
    # Get my orders (sell only for now)
    orders = []
    file_name = os.path.join("./dump/my/myorders.json")
    file_exists = os.path.exists(file_name)
    if bool_refresh or not file_exists:
        print("Downloading orders...") 
        url = "https://api.warframe.market/v2/orders/user/" + str(username)
        download_json(url, file_name)
        print("Done\n")
    # Get list of items (that are visible & sell only)
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            orders = [order for order in data["data"] if (order["type"] == "sell" and order["visible"] == True)]
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    return orders
