from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import query
import pandas
from typing import Union


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get("/orders/", response_class=HTMLResponse)
async def read_items(request: Request, search: str, fulfilled: Union[str, None] = None):
    if search:
        print(f'Querying for {search}')
        search_query = {
            'date_from': '2022-1-01',
            'date_to': '2022-7-07',
            'price_from': 500,
            'price_to': 2000,
            'search': search  # case insensitive
        }
        df = query.query(search_query)  # Pulling initial DF
        df = df[['created_at', 'placed_at', 'order_status', 'sku']]  # Filtering it down to what we need
        html = df.to_html()  # Using Pandas inbuilt html and css function

        order_count = f'<html> <body> <h1>Number of Results:</h1> <p>{(len(df))}.</p> </body> </html>'
        return order_count + html
    else:
        return 404

#  uvicorn main:app --reload
