"""
Analyze data, e.g. get items that are worth the most, or are most sought for.
"""

import time
import matplotlib.pyplot as plt
import pandas as pd
import json
import wgraph

def top_most_traded(file_names, rank=0):
    """Returns most traded items."""
    
    lista = []
    for filename in file_names:
        with open(filename,'r') as f: # check extension?
            data = json.load(f)
        item = []
        name = filename.removesuffix(".json")
        name = name.removeprefix("./dump/items/")
        item.append(name)
        # Reported trades - long term
        longterm_trades_data = data['payload']['statistics_closed']['90days']
        if longterm_trades_data != []:
            df = pd.DataFrame(longterm_trades_data)
            # Fix time
            df['time'] = pd.to_datetime(df['datetime'])
            # If we are looking at mods, only return rank 0
            if 'mod_rank' in df.columns:
                rank0 = df[df['mod_rank'] == rank]
            else:
                rank0 = df
            total_volume = rank0['volume'].sum()
            item.append(total_volume)
            avg_price = rank0['avg_price'].mean()
            item.append(avg_price)
            lista.append(item)
    return lista

def get_lowest_price(file_name, rank):
    with open(file_name, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data["data"])
        df["status"] = df["user"].apply(lambda x: x["status"])
        df_filtered = df[(df["type"] == "sell") & (df["visible"] == True) & ((df["rank"] == rank) if "rank" in df.columns else True) & (df["status"] == "ingame")][["platinum", "quantity", "status"]]
        if df_filtered['platinum'].nsmallest(1).values != None:
            lowest_platinum = df_filtered['platinum'].nsmallest(1).values[0]
        else:
            lowest_platinum = 999
            print("No other item of this kind online was found.")
    return lowest_platinum

def analyze_orders(df):
    for index, row in df.iterrows():
        url = "https://api.warframe.market/v2/orders/item/" + str(row['slug'])
        file_name = "./dump/orders/" + str(row['slug']) + ".json"
        wgraph.download_json(url, file_name)
        print("Checking " + row["Name"] + " .... ", end="")
        my_price = row["platinum"]
        lowest_price = get_lowest_price(file_name, row["rank"])
        print(f"Lowest price: {lowest_price}", end="")
        print(f"   My price: {my_price} ..... ", end="")
        if (my_price - lowest_price) < 0:
            print("\033[31mTOO CHEAP\033[0m")
        elif (my_price - lowest_price) >= 5:
            print("\033[31mTOO EXPENSIVE\033[0m")
        else:
            print("\033[32mOK\033[0m")
        time.sleep(1)

if __name__ == "__main__":

    print("Single item analysis\n\n")
    choice = input("Name of the item to analyze?\n")
    # Generate the URL from the item's name
    url = wgraph.make_pair(choice)
    # Fetch json file and save to disk if needed(cache)
    wgraph.fetch_json_and_save(url)
    # Open downloaded json file
    json_file_name = url[0]
    print("Opening " + json_file_name)
    with open(json_file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        name = json_file_name.removesuffix(".json")
        name = name.removeprefix("./dump/items/")
    rank = input("Rank to check?\n")
    print(data["payload"]["statistics_live"]["90days"])
    records = [entry for entry in data["payload"]["statistics_live"]["90days"] if entry["mod_rank"] == rank]
    print(records)
    df = pd.DataFrame(records)
    print(df["datetime"])
    df["datetime"] = pd.to_datetime(df["datetime"][0:10])
    df.sort_values("datetime", inplace=True)

    # Calculate moving average of avg_price (window=2 for illustration; adjust as needed)
    df["moving_avg"] = df["avg_price"].rolling(window=2, min_periods=1).mean()

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar plot for volume
    ax1.bar(df["datetime"], df["volume"], color="lightgrey", label="Volume", width=0.03)
    ax1.set_ylabel("Volume", color="grey")
    ax1.tick_params(axis='y', labelcolor='grey')

    # Create second y-axis for prices
    ax2 = ax1.twinx()

    # Plot min, max, avg, and moving average
    ax2. plot(df["datetime"], df["min_price"], label="Min Price", marker="o", color="green")
    ax2.plot(df["datetime"], df["max_price"], label="Max Price", marker="o", color="red")
    ax2.plot(df["datetime"], df["avg_price"], label="Avg Price", marker="o", color="blue")
    ax2.plot(df["datetime"], df["moving_avg"], label="Moving Avg", linestyle="--", color="orange")

    ax2.set_ylabel("Price")
    ax2.legend(loc="upper left")

    plt.title("Price Statistics & Volume (mod_rank=0)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    #download_and_save(item)
    
    #with open(item[0],'r') as f: # check extension?
    #    data = json.load(f)
    #    print(data)


    
