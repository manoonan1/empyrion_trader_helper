#!/usr/bin/env python
# coding: utf-8

# In[143]:


import pandas as pd
import re


# In[144]:


df = pd.read_csv("eden_traders.csv")
df = df.replace(r'\n',' ', regex=True)

df["trader sells"] = df["trader sells"].fillna('Does Not Sell')
df["trader buys"] = df["trader buys"].fillna('Does Not Buy')


# In[145]:


def findName(df, input_name):
    return df.loc[df['name'] == input_name]
    
#print(findName(df, "Unsanctioned Goods"))


# In[146]:


def findPOI(df, input_name):
    return df.loc[df['poi'] == input_name]

#print(findPOI(df, "Distribution Headquarters"))


# In[147]:


def findPlayfield(df, input_name):
    return df.loc[df['playfield'] == input_name]

#print(findPlayfield(df, "Distribution Headquarters"))


# In[148]:


def findSellers(df, input_item):
    sells = df[df['trader sells'].str.contains(input_item)]
    items = pd.DataFrame(columns = ['name', 'market_value', 'in_stock'])
    for index, row in sells.iterrows():
        item = re.findall((rf"(?i){re.escape(input_item)}: \d{{1,}}.\d{{1,}}-\d{{1,}}.\d{{1,}},\d{{1,}}-\d{{1,}}"), sells["trader sells"][index])
        market_value = re.findall((r'\d{1,}\.\d{1,}-\d{1,}\.\d{1,}'), str(item))
        if not market_value: 
            item = re.findall((rf"(?i){input_item}: \d{{1,}}-\d{{1,}},\d{{1,}}-\d{{1,}}"), sells["trader buys"][index])
            market_value = re.findall((r'\d{1,}-\d{1,}'), str(item))
        in_stock = re.findall((r'\d{1,}-\d{1,}'), str(item))
        
        new_row = pd.Series({'name' : sells["name"][index], 'market_value' : str(market_value[0]), 'in_stock' : str(in_stock[1])})
        items = pd.concat([items, new_row.to_frame().T], ignore_index = True)
    return items


# In[149]:


def findBuyers(df, input_item):
    buys = df[df['trader buys'].str.contains(input_item)]
    items = pd.DataFrame(columns = ['name', 'market_value', 'will_buy'])
    for index, row in buys.iterrows():
        item = re.findall((rf"(?i){re.escape(input_item)}: \d{{1,}}.\d{{1,}}-\d{{1,}}.\d{{1,}},\d{{1,}}-\d{{1,}}"), buys["trader buys"][index], flags=re.IGNORECASE)
        market_value = re.findall((r'\d{1,}\.\d{1,}-\d{1,}\.\d{1,}'), str(item))
        if not market_value: 
            item = re.findall((rf"(?i){input_item}: \d{{1,}}-\d{{1,}},\d{{1,}}-\d{{1,}}"), buys["trader buys"][index])
            market_value = re.findall((r'\d{1,}-\d{1,}'), str(item))
        in_stock = re.findall((r'\d{1,}-\d{1,}'), str(item))
        
        new_row = pd.Series({'name' : buys["name"][index], 'market_value' : str(market_value[0]), 'will_buy' : str(in_stock[1])})
        items = pd.concat([items, new_row.to_frame().T], ignore_index = True)
    return items


# In[150]:


def findBestBuyPrices(df, input_item):
    buyers = findBuyers(df, input_item)
    for index, row in buyers.iterrows():
        buyers["market_value"][index] = buyers["market_value"][index].split("-")
        buyers["market_value"][index] = (float(buyers["market_value"][index][0])+float(buyers["market_value"][index][1]))/2
    return buyers[buyers.market_value == buyers.market_value.max()]

#findBestBuyPrices(df, "Iron Ingot")


# In[151]:


def findBestSellPrices(df, input_item):
    sellers = findSellers(df, input_item)
    for index, row in sellers.iterrows():
        sellers["market_value"][index] = sellers["market_value"][index].split("-")
        sellers["market_value"][index] = (float(sellers["market_value"][index][0])+float(sellers["market_value"][index][1]))/2
    return sellers[sellers.market_value == sellers.market_value.min()]

#findBestSellPrices(df, "Gold Ingot")


# In[152]:


def findTradeRoute(df, input_item):
    
    items = pd.DataFrame(columns = ['buy_from', 'in_stock', 'sell_to','will_buy','avg_margin'])
    bestSellers = findBestBuyPrices(df, input_item)
    bestBuyers = findBestSellPrices(df, input_item)
    
    bestBuyers = bestBuyers.merge(bestSellers, how='cross')
    items = bestBuyers
                                          
    items.rename(columns={'name_x': 'buy_from','market_value_x': 'buy_rate', 'name_y': 'sell_to',
                             'market_value_y': 'sell_rate'}, inplace=True)
    return items


# In[159]:


def consoleOutputHandler(option):
    match option:

        #output implementation #looking to sell
        case '1':
            item_to_sell = input('\nWhat item are you looking to sell? ')
            print("\n")
            print(findBuyers(df, item_to_sell))
            
        #output implementation #looking to buy
        case '2':
            item_to_buy = input('\nWhat item are you looking to buy? ')
            print("\n")
            print(findSellers(df, item_to_buy))

        #output implementation #looking for best place to buy
        case '3':
            item_to_buy = input('\nWhat item are you looking to buy? ')
            print("\n")
            print(findBestSellPrices(df, item_to_buy))

        #output implementation #looking for best place to sell
        case '4':
            item_to_sell = input('\nWhat item are you looking to sell? ')
            print("\n")
            print(findBestBuyPrices(df, item_to_sell))

        #output implementation #looking for trade route
        case '5':
            item_to_trade = input('\nWhat item are you looking to find a trade route for? ')
            print("\n")
            print(findTradeRoute(df, item_to_trade))
        
        case _:
            print("\nThe input is not an option listed.")


# In[169]:


print("Please input the following option for your needs:")
print("(1): Looking to sell")
print("(2): Looking to buy")
print("(3): Looking for best place to sell")
print("(4): Looking for best place to buy")
print("(5): Looking for trade route\n")

option = input("option? ")

consoleOutputHandler(option)


# In[ ]:




