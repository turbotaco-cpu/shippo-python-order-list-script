# import requests
# #temporarily hacked it with max results of 250 for testing purposes.
# token = "shippo_test_277121c5f998ea6f1c5402ca4644ead68662ee57"
# url = 'https://api.goshippo.com/orders?results=250'
# headers = {'Authorization': 'ShippoToken token'}
# r = requests.get(url, headers=headers)
# orders = r.json()
# r.json()

# import json
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(orders, f, ensure_ascii=False, indent=4)
# #dumps json so we don't go to API every time

# load pandas and json modules
# loads JSON from local file so I don't have to constantly hit the API for the same thing
import pandas as pd
import json
import re

# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary and creates the orders variable
orders = json.load(f)

# this handles the object info--but not deeper into the tree such as line items
order_list = pd.json_normalize(
    orders['results'],
)

# looping through the dataframe and conditionally checking for an SKU whilst providing error handling
# The resulting list is added as a new column to the checked data frame
# Essentially it's manual normalization with conditions

pd.set_option("display.max.rows", 15)

sku_list = []
for index, row in order_list.iterrows():
    if len(row['line_items']) > 0:
        sku = (row['line_items'][0]['sku'])
        sku_list.append(sku)
    else:
        sku_list.append('Empty')

order_list["sku"] = sku_list

# order_list

# converting from string to date-time
# doing it twice because there are two different formats involved as SHippo API changed
format_string = "%Y-%m-%dT%H:%M:%SZ"
date1 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')
date2 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%SZ')
order_list['created_at'] = date1.fillna(date2)

# converting string to float for prices so they can be searched
order_list['subtotal_price'] = order_list['subtotal_price'].astype(float)
order_list['total_price'] = order_list['total_price'].astype(float)

pd.set_option('display.max_rows', 100)
date_from = '2021-12-01'
date_to = '2021-12-31'
price_from = 0
price_to = 1300
search = '45'  # case insensitive

# now we can filter by date and add several conditions together with bools.
# The flag parameter is also used and re.I is passed to it, which means IGNORECASE.
# https://www.geeksforgeeks.org/python-pandas-series-str-count/

filtered_df = order_list.loc[
    (order_list['created_at'] >= date_from)
    & (order_list['created_at'] <= date_to)
    & order_list['sku'].str.count(search, re.I)
    & (order_list['subtotal_price'] >= price_from)
    & (order_list['subtotal_price'] <= price_to)
    ]

msg = (
    f'Date From: {date_from}\nDate To: {date_to}\n'
    f'Price From: ${price_from}\nPrice To: ${price_to}\nSearch Term: "{search}"'
)
print(msg)
subtotal_total = filtered_df['subtotal_price'].sum()
order_total = (len(filtered_df))
print(f"\nSubtotal Total: ${subtotal_total}")
print(f"Number of Orders: {order_total}")
# filtered_df[['sku','subtotal_price', 'total_price', 'shop_app']]
