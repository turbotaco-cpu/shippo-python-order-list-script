import re
import pandas as pd


def filter_orders(date_from: str,
                  date_to: str,
                  price_from: int,
                  price_to: int,
                  search: str,
                  modified_df: pd.DataFrame):

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
