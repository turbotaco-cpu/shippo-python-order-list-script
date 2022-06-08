import json
import pandas as pd
import requests


def get_shippo_json(token: str, url: str, json_filename: str,
                    refresh_json: bool) -> pd.DataFrame:

    if refresh_json:
        # Pull from REST api
        headers = {'Authorization': 'ShippoToken ' + token}
        print(headers)
        r = requests.get(url, headers=headers)
        orders = r.json()

        # Create JSON file
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=4)
            print(f"OK {json_filename} file saved")
        return orders
    else:
        try:
            f = open(json_filename)
            orders = json.load(f)
            print('JSON file found and opened!')
            return orders
        except FileNotFoundError:
            print(f"The file {json_filename} cannot be found.")
