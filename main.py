import pandas as pd
import json
import re
from typing import List
import get_shippo_json


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


if __name__ == '__main__':
    refresh_json = False
    pd.set_option('display.max_rows', 100)
    # Order search options:
    date_from = '2021-12-01'
    date_to = '2021-12-31'
    price_from = 0
    price_to = 1300
    search = '45'  # case insensitive

    # hacked it temporarily with max results--pagination is advisable
    json_filename = 'data.JSON'
    token = 'shippo_test_11e5a116bb4d1769263755c5cad312a868c184d3'
    url = 'https://api.goshippo.com/orders?results=250'

    orders = get_shippo_json.get_shippo_json(token, url, json_filename, refresh_json)

    # this handles the object info--but not deeper into the tree such as line items
    order_df = pd.json_normalize(
        orders['results'],
    )

    print(type(order_df))

    datatime_fixed_df = fix_shippo_json(order_df)
    filter_orders(date_from, date_to, price_from, price_to, search, datatime_fixed_df)
