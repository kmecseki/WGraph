"""
Analyze data, e.g. get items that are worth the most, or are most sought for.
"""

import matplotlib.pyplot as plt
import pandas as pd
import json
import os

def top_most_traded(only_listed=True):
    """Returns most traded items."""

    if only_listed:
        to_check = []
        with open("Suda.txt",'r') as suda:
            for r in suda:
                to_check.append(r.removesuffix('\n'))
    lista = []
    for fname in os.listdir("./dump/"):
        if fname.endswith(".json"):
            filename = os.path.join("./dump", fname)
            with open(filename,'r') as f: # check extension?
                data = json.load(f)
        item = []
        name = fname.removesuffix(".json")
        if only_listed:
            if name in to_check:
                item.append(name)
        else:
            item.append(name)
        # Reported trades - long term
        longterm_trades_data = data['payload']['statistics_closed']['90days']
        if longterm_trades_data != []:
            df = pd.DataFrame(longterm_trades_data)
            # Fix time
            df['time'] = pd.to_datetime(df['datetime'])
            # If we are looking at mods, only return rank 0
            if 'mod_rank' in df.columns:
                rank0 = df[df['mod_rank'] == 0]
            else:
                rank0 = df
            total_volume = rank0['volume'].sum()
            item.append(total_volume)
            avg_price = rank0['avg_price'].mean()
            item.append(avg_price)
            lista.append(item)
    return lista

# Return only suda ones
only_listed = True

# Number of items to look at
number_of_items = 50

lista = top_most_traded(only_listed)
df2 = pd.DataFrame(lista)
df2.columns = ['name', 'volume', 'avg_price']
top = df2.sort_values(by='volume', ascending=False).head(number_of_items)
print(top)





