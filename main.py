# TODO wrap the requests and online api download into a function

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

# loads JSON from local file to avoid constant API requests
import pandas as pd
import json
import re
from typing import List


# TODO fix typing as it's being used with Pandas DF and with nothing it doesn't work


def load_json(file: str) -> pd.DataFrame:
    f = open(file)
    # returns JSON object as a dictionary and creates the orders variable
    orders = json.load(f)

    # this handles the object info--but not deeper into the tree such as line items
    order_list = pd.json_normalize(
        orders['results'],
    )

    print(type(order_list))
    return order_list


json_file = "data.json"
order_df = load_json(json_file)


def fix_shippo_json(order_list: pd.DataFrame) -> pd.DataFrame:
    pd.set_option("display.max.rows", 15)
    # looping through the dataframe and conditionally checking for an SKU whilst providing error handling
    # The resulting list is added as a new column to the checked data frame
    # Essentially it is manual normalization with conditions
    sku_list = []
    for index, row in order_list.iterrows():
        if len(row['line_items']) > 0:
            sku = (row['line_items'][0]['sku'])
            sku_list.append(sku)
        else:
            sku_list.append('Empty')
            # fills in the data as there were no SKUs at a certain time

    order_list["sku"] = sku_list

    # converting from string to date-time
    # doing it twice because there are two different formats involved as SHippo API changed
    # it will look for datetime twice--and then fill together so everything is fixed
    date1 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')
    date2 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%SZ')
    order_list['created_at'] = date1.fillna(date2)

    # converting string to float for prices so they can be searched
    # TODO not use float but also retain price accurately enough
    order_list['subtotal_price'] = order_list['subtotal_price'].astype(float)
    order_list['total_price'] = order_list['total_price'].astype(float)
    return order_list


datatime_fixed_df = fix_shippo_json(order_df)


def filter_orders(date_from: str,
                  date_to: str,
                  price_from: int,
                  price_to: int,
                  search: str,
                  datatime_fixed_df):
    # now we can filter by date and add several conditions together with bools.
    # The flag parameter is also used and re.I is passed to it, which means IGNORECASE.
    # https://www.geeksforgeeks.org/python-pandas-series-str-count/

    filtered_df = datatime_fixed_df.loc[
        (datatime_fixed_df['created_at'] >= date_from)
        & (datatime_fixed_df['created_at'] <= date_to)
        & datatime_fixed_df['sku'].str.count(search, re.I)
        & (datatime_fixed_df['subtotal_price'] >= price_from)
        & (datatime_fixed_df['subtotal_price'] <= price_to)
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


pd.set_option('display.max_rows', 100)
date_from = '2021-12-01'
date_to = '2021-12-31'
price_from = 0
price_to = 1300
search = '45'  # case insensitive

filter_orders(date_from, date_to, price_from, price_to, search, datatime_fixed_df)
