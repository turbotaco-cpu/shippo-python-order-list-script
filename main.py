from typing import List
import get_shippo_json
import fix_shippo_json
import filter_orders
import os


if __name__ == '__main__':
    refresh_json = True
    # Order search options:
    date_from = '2021-12-01'
    date_to = '2022-5-31'
    price_from = 0
    price_to = 1300
    search = '45'  # case insensitive

    # TODO fix the enviroment variable and make it secure
    # hacked it temporarily with max results--pagination is advisable
    json_filename = 'data.JSON'
    token = "shippo_test_0dad27695d44e07b07d643ee4782f516c2ad98ee"
    blank = os.environ.get('token')
    # Could put token here in plaintext if absolutely needed
    url = 'https://api.goshippo.com/orders?results=250'

    orders_df = get_shippo_json.get_shippo_json(token, url, json_filename, refresh_json)

    print(type(orders_df))

    datatime_fixed_df = fix_shippo_json.fix_shippo_json(orders_df)
    filter_orders.filter_orders(date_from, date_to, price_from, price_to, search, datatime_fixed_df)
