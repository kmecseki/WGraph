
import pandas as pd
from wgraph import getitems, download_and_save
import analyze


if __name__ == "__main__":

    # get item names 
    choice = input("What items do you want to check?\n 1. Arcanes\n 2. Mods\n 3. Prime parts and sets\n 4. Non-prime parts\n 5. Relics\n 6. Single item statistics\n")
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
                        case "4":
                            choice4 = input("1. Suda\n 2. Hexis\n 3. New Loka\n 4. Steel Meridian\n")
                            match choice4:
                                case "1":
                                    items = getitems("Suda")
                                case "2":
                                    items = getitems("Hexis")
                                case "3":
                                    items = getitems("Loka")
                                case "4":
                                    items = getitems("Steel")
                case "2":
                    choice3 = input(" 1. Warframe\n 2. Primary\n 3. Secondary\n 4. Melee\n 5. Companion\n 6. Railjack\n 7. Archwing\n")
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
                case "3":
                    items = getitems("mod")
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
    
    proceed = input("This will be " + str(len(items)) + " items. Proceed?")
    if proceed == "yes" or proceed == "y" or proceed == "Yes" or proceed == "Y":
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

            


