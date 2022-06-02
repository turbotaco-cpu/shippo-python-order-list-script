# converting from string to date-time
# doing it twice because there are two different formats involved as SHippo API changed
format_string = "%Y-%m-%dT%H:%M:%SZ"
date1 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%fZ')
date2 = pd.to_datetime(order_list['created_at'], errors='coerce', format='%Y-%m-%dT%H:%M:%SZ')
order_list['created_at'] = date1.fillna(date2)

# converting string to float for prices so they can be searched
order_list['subtotal_price'] = order_list['subtotal_price'].astype(float)
order_list['total_price'] = order_list['total_price'].astype(float)