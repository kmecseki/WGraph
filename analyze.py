"""
Analyze data, e.g. get items that are worth the most, or are most sought for.
"""

import matplotlib.pyplot as plt
import pandas as pd
import json
import os

def top10_most_traded():
    """Returns most traded items."""
    
    lista = []
    for fname in os.listdir("./dump/"):
        if fname.endswith(".json"):
            filename = os.path.join("./dump", fname)
            with open(filename,'r') as f: # check extension?
                data = json.load(f)
        item = []
        item.append(fname.removesuffix(".json"))
        # Reported trades - long term
        longterm_trades_data = data['payload']['statistics_closed']['90days']
        if longterm_trades_data != []:
            df = pd.DataFrame(longterm_trades_data)
            # Fix time
            df['time'] = pd.to_datetime(df['datetime'])
            # Only rank 0
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

lista = top10_most_traded()
df2 = pd.DataFrame(lista)
df2.columns = ['name', 'volume', 'avg_price']
top10 = df2.sort_values(by='volume', ascending=False).head(50)
print(top10)





