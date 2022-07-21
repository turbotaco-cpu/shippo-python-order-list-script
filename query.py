import os
from typing import List
import get_shippo_json
import fix_shippo_json
import filter_orders
from dotenv import load_dotenv

load_dotenv()

""" 
TODO Have the JSON request reflect desired date range as per Shippo docs
https://goshippo.com/docs/orders/#:~:text=You%20can%20retrieve%20an%20order,of%20our%20shopping%20cart%20integrations.

Flow might want to be the following:
- User decides if they want to see all orders or date ranged.

- If date range is selected the query will only call what is needed.
- If user requests all data then pagination is used

- Regardless in both cases the date range of the initial query 
"""


def query(search_query):
    # Pagination suggested--hacked with max result = 250
    # ToDO decide on method for pagination and implement it.

    # Get token from .env file
    json_filename = 'data.JSON'
    refresh_json = False
    token = os.environ.get('TOKEN')
    url = 'https://api.goshippo.com/orders?results=250'

    #  Sourcing JSON and Creating Data Frame DF:
    orders_df = get_shippo_json.get_shippo_json(token, url, json_filename, refresh_json)

    #  Fixing any datetime conflicts:
    datatime_fixed_df = fix_shippo_json.fix_shippo_json(orders_df)

    #  Filtering orders using search query options, prints results, and returns the filtered dataframe:
    return filter_orders.filter_orders(search_query, datatime_fixed_df)


if __name__ == '__main__':
    # Order search options:
    search_query = {
        'date_from': '2022-1-01',
        'date_to': '2022-7-07',
        'price_from': 500,
        'price_to': 2000,
        'search': ''  # case insensitive
    }
    query(search_query)
