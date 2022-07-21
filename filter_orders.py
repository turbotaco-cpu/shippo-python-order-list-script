import re
import pandas as pd
from operator import itemgetter


def filter_orders(search_query: dict, modified_df: pd.DataFrame):
    #  Unpacking the search query dict which was passed in:
    date_from, date_to, search, price_from, price_to = \
        itemgetter('date_from', 'date_to', 'search', 'price_from', 'price_to')(search_query)

    filtered_df = modified_df.loc[
        (modified_df['created_at'] >= date_from)
        & (modified_df['created_at'] <= date_to)
        & modified_df['sku'].str.count(search, re.I)
        # re.I is case-insensitive REGEX
        & (modified_df['subtotal_price'] >= price_from)
        & (modified_df['subtotal_price'] <= price_to)
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

    return filtered_df
