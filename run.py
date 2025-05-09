import os
import json
import datetime
import time
import pandas as pd
from wgraph import getitems, download_and_save, get_current_orders, download_json
import analyze
from kubrow import lastkubrow

if __name__ == "__main__":

    os.makedirs("./dump", exist_ok=True)
    os.makedirs("./dump/items/", exist_ok=True)
    os.makedirs("./dump/my/", exist_ok=True)
    os.makedirs("./dump/orders/", exist_ok=True)
    choice = input("What items do you want to check?\n 1. Arcanes\n 2. Mods\n 3. Prime parts and sets\n 4. Non-prime parts\n 5. Relics\n 6. Single item statistics\n 7. Analyze current orders\n 8. Live alert\n 9. Kubrow colors\n")
    items = []
    match choice:
        case "1":
            items = getitems("arcane_enhancement")
        case "2":
            choice2 = input("By rarity or function?\n 1. Rarity\n 2. Function\n 3. All mods\n 4. Syndicate\n")
            match choice2:
                case "1":
                    choice3 = input(" 1. Common\n 2. Uncommon\n 3. Rare\n")
                    match choice3:
                        case "1":
                            items = getitems("mod", "common")
                        case "2":
                            items = getitems("mod", "uncommon")
                        case "3":
                            items = getitems("mod", "rare")
                case "2":
                    choice3 = input(" 1. Warframe\n 2. Primary\n 3. Secondary\n 4. Melee\n 5. Companion\n 6. Railjack\n 7. Archwing\n 8. Aura\n")
                    match choice3:
                        case "1":
                            items = getitems("mod", "warframe")
                        case "2":
                            items = getitems("mod", "primary")
                        case "3":
                            items = getitems("mod", "secondary")
                        case "4":
                            items = getitems("mod", "melee")
                        case "5":
                            items = getitems("mod", "companion")
                        case "6":
                            items = getitems("mod", "railjack")
                        case "7":
                            items = getitems("mod", "archwing")  
                        case "8":
                            items = getitems("mod", "aura")
                case "3":
                    items = getitems("mod")
                case "4":
                    choice4 = input("1. Suda\n 2. Hexis\n 3. New Loka\n 4. Steel Meridian\n 5. Perrin Sequence\n 6. Red Veil\n")
                    match choice4:
                                case "1":
                                    items = getitems("Suda")
                                case "2":
                                    items = getitems("Hexis")
                                case "3":
                                    items = getitems("Loka")
                                case "4":
                                    items = getitems("Steel")
                                case "5":
                                    items = getitems("Perrin")
                                case "6":
                                    items = getitems("Red")
        case "3":
            choice3 = input("1. Warframe primes\n 2. Primary primes\n 3. Secondary primes\n 4. Melee primes\n 5. Companion primes\n 6. All primes\n")
            match choice3:
                case "1":
                    items = getitems("prime", "warframe")
                case "2":
                    items = getitems("prime", "primary")
                case "3":
                    items = getitems("prime", "secondary")
                case "4":
                    items = getitems("prime", "melee")
                case "5":
                    items = getitems("prime", "companion")
                case "6":
                    items = getitems("prime")
        case "4":
            items = getitems("weapon", no=["prime"])
        case "5":
            choice3 = input(" 1. Lith\n 2. Meso\n 3. Neo\n 4. Axi\n 5. All relics\n")
            match choice3:
                case "1":
                    items = getitems("relic", "lith")
                case "2":
                    items = getitems("relic", "meso")
                case "3":
                    items = getitems("relic", "neo")
                case "4":
                    items = getitems("relic", "axi")
                case "5":
                    items = getitems("relic")
        case "6":
            filename = input("Name of the item? E.g.  Molt Vigor")
            with open(os.path.join("./items/wfm-items/tracked/items/"\
                               ,filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                item = url_gen(data)
            exit(0)
        case "7":
            # Get my orders
            refresh_orders = input("Refresh orders? Default: yes\n")
            bool_refresh_orders = (refresh_orders == "" or refresh_orders == "yes" or refresh_orders == "y" or refresh_orders == "Yes" or refresh_orders == "Y")
            orders = get_current_orders("Kat78", bool_refresh_orders)

            # Get item list
            refresh_items = input("Refresh items? Default: no\n")
            bool_refresh_items = (refresh_orders == "yes" or refresh_orders == "y" or refresh_orders == "Yes" or refresh_orders == "Y")
            file_name = os.path.join("./dump/my/items.json")
            url = "https://api.warframe.market/v2/items"
            if not os.path.exists(file_name) or bool_refresh_items:
                print("Downloading items file...")
                download_json(url, file_name)
                print("Done")
            
            df = pd.DataFrame(orders)[['platinum', 'rank', 'quantity', 'itemId']]
            # Match ids with names
            with open(file_name, "r") as f:
                items_data = json.load(f)
                item_map_name = {item['id']: item['i18n']['en']['name'] for item in items_data['data']}
                item_map_slug = {item['id']: item['slug'] for item in items_data['data']}

            df['Name'] = df['itemId'].map(item_map_name)
            df['slug'] = df['itemId'].map(item_map_slug)
            df = df.fillna(0.0)
            analyze.analyze_orders(df)
            exit(0)
        case "8":
            # Take item name
            item_name = input("Item name?:\n")
            url_item_name = item_name.replace(" ", "_").replace("'", "").lower()
            rank = input("If this is a mod, rank? Otherwise just type 0.\n")
            url = "https://api.warframe.market/v2/orders/item/" + str(url_item_name)
            file_name = os.path.join("./dump/my/" + str(url_item_name) + "livealert.json")
            price_wanted = input("Price wanted?\n")
            while not price_wanted.isdigit() and int(price_wanted) <= 0:
                price_wanted = input("Price wanted?:\n")
            is_correct = input("Item name: " + str(item_name) + ". The full url will be: " + url + " for " + str(price_wanted) + ". Is this correct? Default: yes\n")
            bool_is_correct = (is_correct == "yes" or is_correct == "y" or is_correct == "Yes" or is_correct == "Y" or is_correct == "")
            while bool_is_correct:
                print("Checking...")
                download_json(url, file_name)
                lowest_price = analyze.get_lowest_price(file_name, rank)
                if lowest_price <= int(price_wanted):
                    print("Found one for " + str(lowest_price) + "!!!!")
                    bool_is_correct = False
                else:
                    print("Current lowest price is: " + str(lowest_price) + ". Waiting 60 sec before trying again...")
                    time.sleep(60)
            exit(0)
            
            # Keep checking
            # When there is a hit, write out something and exit
        case "9":
            print("")
            lastkubrow()
            print("")
            exit(0)

    proceed = input("This will be " + str(len(items)) + " items. Proceed?")
    if proceed == "" or proceed == "yes" or proceed == "y" or proceed == "Yes" or proceed == "Y":
        download_and_save(items)
    
        # Get a list of the item names
        file_names = []
        for item in items:
            file_names.append(item[0])
        rank = 0
        if choice == "1":
            choice2 = input("Arcane rank to check? \n 1. Maxed\n 2. Unranked\n")
            rank = 5 if choice2 == "1" else 0
        choice0 = input("Analyze:\n 1. Top most traded\n 2. Top highest price\n")
        number_of_items = 50
        lista = analyze.top_most_traded(file_names, rank)
        df2 = pd.DataFrame(lista)
        df2.columns = ['name', 'volume', 'avg_price']
        match choice0:
            case "1":
                top = df2.sort_values(by='volume', ascending=False).head(number_of_items)
                print(top)
            case "2":
                top = df2.sort_values(by='avg_price', ascending=False).head(number_of_items)
                print(top)

            


