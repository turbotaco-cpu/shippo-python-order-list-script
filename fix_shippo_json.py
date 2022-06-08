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

    # Converting from string to date-time
    # Using coerce error handle--we handle both cases and merge the results together
    date1 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')
    date2 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%SZ')
    order_list['created_at'] = date1.fillna(date2)

    # Converting string to float for prices so they can be searched
    # TODO see if better option than float or limit float accuracy
    order_list['subtotal_price'] = order_list['subtotal_price'].astype(float)
    order_list['total_price'] = order_list['total_price'].astype(float)
    return order_list
