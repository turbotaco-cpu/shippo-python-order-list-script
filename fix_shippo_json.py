import pandas as pd


def fix_shippo_json(order_list_in: pd.DataFrame) -> pd.DataFrame:

    order_list = pd.json_normalize(
        order_list_in['results'],
    )

    # looping through the dataframe and conditionally checking for an SKU whilst providing error handling
    # The resulting list is added as a new column to the checked data frame
    sku_list = []
    for index, row in order_list.iterrows():
        if len(row['line_items']) > 0:
            sku = (row['line_items'][0]['sku'])
            sku_list.append(sku)
        else:
            sku_list.append('Empty')
            # fills in the data as there were no SKUs at a certain time

    order_list["sku"] = sku_list

    # Converting from string to date-time using Pandas
    date1 = pd.to_datetime(order_list['placed_at'], errors='raise', exact=False, infer_datetime_format=True, format='%Y-%m-%d %H:%M')
    order_list['created_at'] = date1

    # Converting string to float for prices so they can be searched
    order_list['subtotal_price'] = order_list['subtotal_price'].astype(float)
    order_list['total_price'] = order_list['total_price'].astype(float)
    return order_list
