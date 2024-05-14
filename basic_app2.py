from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)


@app.get("/store")
def get_store():
    return {"stores": list(stores.values())}

@app.get("/item")
def get_items():
    return {"items": list(items.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if (
        "name" not in store_data
    ):
        abort(404,
        message="Bad Requet, Ensure name is included in Json Payload"
        )
    for store in stores:
        if store_data["name"] == store["name"]:
            abort(404, messgae="Store already exist")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id]=store
    return store, 201

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store Deleted"}
    except KeyError:
        abort(404, messeage="store not found.")

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            messeage="Bad request, Ensure 'price', 'name' and 'store_id' are included in Json Payload"
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(
                400,
                message="Item already exist"
            )
    if item_data['store_id'] not in stores:
        abort(404, messeage="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id]=item
    return item, 201
   
@app.get("/store/<string:store_id>")
def get_specific_store_details(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, messeage="Store not found.") 

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, messeage="item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item Deleted"}
    except KeyError:
        abort(404, messeage="item not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data or "price" not in item_data:
        abort(
            400,
            messeage="Bad request, Ensure 'price', 'name' and 'store_id' are included in Json Payload"
        )

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, messeage="item not found.")
