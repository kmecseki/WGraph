
import pandas as pd
from wgraph import getitems, download_and_save
import analyze


if __name__ == "__main__":

    # get item names 
    choice = input("What items do you want to check?\n 1. Arcanes\n 2. Mods\n 3. Prime parts and sets\n 4. Non-prime parts\n 5. Relics\n ")
    items = []
    match choice:
        case "1":
            items = getitems("arcane_enhancement")
        case "2":
            choice2 = input("By rarity or function?\n 1. Rarity\n 2. Function\n 3. All mods\n")
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
                    choice3 = input(" 1. Warframe\n 2. Primary\n 3. Secondary\n 4. Melee\n 5. Companion\n 6. Railjack\n 7. Suda\n 8. Hexis\n")
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
                            items = getitems("Suda")
                        case "8":
                            items = getitems("Hexis")
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
            items = getitems("weapon", no="prime")
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

    proceed = input("This will be " + str(len(items)) + " items. Proceed?")
    if proceed == "yes" or proceed == "y" or proceed == "Yes" or proceed == "Y":
        download_and_save(items)
    
        # Get a list of the item names
        file_names = []
        for item in items:
            file_names.append(item[0])
        choice = input("Analyze: 1. Top most traded\n")
        match choice:
            case "1":
                number_of_items = 50

                lista = analyze.top_most_traded(file_names)
                df2 = pd.DataFrame(lista)
                df2.columns = ['name', 'volume', 'avg_price']
                top = df2.sort_values(by='volume', ascending=False).head(number_of_items)
                print(top)
            


