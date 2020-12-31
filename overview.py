import pandas as pd
from tqdm import tqdm

item = pd.DataFrame()


def initDataO():
    global item
    item = pd.read_csv("item_overview.csv")


def overview():
    # Print the item overview data
    print("========== STATS OVERVIEW ==========")
    bTotal=item['quantity'].sum()
    cTotal=item['clicks'].sum()
    print('Total number of selled items: '+str(bTotal))
    print('Total clicks: '+str(cTotal))
    print('Percentage of buying: '+str((bTotal/cTotal)*100)+"%")
    print("\n")
    

def popular(disp = 5):
    # Get popular items data
    #disp = int(input("Display TOP ? items:"))
    print("========== TOP "+str(disp)+" MOST PURCHASED ==========")
    print(item.sort_values(by='clicks',ascending=False).head(disp).to_string(index=False))
    print("\n")
    print("========== TOP "+str(disp)+" MOST CLICKED ==========")
    print(item.sort_values(by='quantity',ascending=False).head(disp).to_string(index=False))
    print("\n")
    

def itemStat(item_id):
    sitem=item.loc[item['item_id'] == item_id]
    if sitem.empty:
        print("No Result! Change an item_id and try again.")
        return -1
    else:
        print("========== ITEM STATS ==========")
        print(sitem.to_string(index=False))
        return 0