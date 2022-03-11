from typing import List
from flask import Flask, request, jsonify, Response
import os
import re
from tinydb import TinyDB, where
import time

from tinydb.queries import Query

# creates folder if they don't exist
if not os.path.isdir("storages"): os.mkdir("storages")

items = TinyDB("storages/items.db")

# Utils
def has_item(item_name: str): 
    return items.contains(Query().name==item_name)

def has_keys(_keys: List[str], _list: List[str]) -> bool:
    return set(_keys).issubset(set(_list))

# Flask app
api = Flask(__name__)

@api.errorhandler(AssertionError)
def failed(error):
    return "failed - "+str(error), 400

@api.errorhandler(404)
def api_fallback(error):
    return "invalid request", 400

@api.errorhandler(Exception)
def any_fail(error):
    return "failed - "+str(error), 403

@api.route("/list")
def get_all():
    return jsonify(items.all()), 200

@api.route("/item")
def get():
    assert has_keys(["item_name"], request.args.keys()), "bad keys"
    return jsonify(items.get(Query().name == request.args["item_name"])), 200

@api.route("/additem")
def additem():
    global items
    assert has_keys(["item_name", "item_cost", "item_amount"], request.args.keys()), "bad keys"
    assert not has_item(request.args["item_name"]), "bad item"
    assert re.match("[A-Za-z0-9+]", request.args["item_name"]), "bad format"
    assert re.match("[0-9+]", request.args["item_amount"]), "bad format"
    assert re.match("[0-9+]", request.args["item_amount"]), "bad format"

    items.insert({
        "name":request.args["item_name"],
        "cost":int(request.args["item_cost"]),
        "amount":int(request.args["item_amount"])
    })

    return "success", 200

@api.route("/delete")
def delete():
    global items
    # check for requiered keys
    assert has_keys(["item_name"], request.args.keys()), "bad keys"
    assert has_item(request.args["item_name"]), "bad item"
    assert re.match("[A-Za-z0-9+]", request.args["item_name"]), "bad format"

    items.remove(where("name") == request.args["item_name"])
    
    return "success", 200
        
@api.route("/buy")
def buy():
    global items
    # check for required keys
    assert has_keys(["item_name", "item_amount"], request.args.keys()), "bad keys"
    assert has_item(request.args["item_name"]), "bad item"
    assert re.match("[0-9]+", request.args["item_amount"]), "bad format"
    assert items.get(Query().name==request.args["item_name"]).get("amount")-int(request.args["item_amount"])<0, "item overload"
    
    items.update({
        "amount":items.get(Query().name==request.args["item_name"]).get("amount")-int(request.args["item_amount"]),
        }, where("name") == request.args["item_name"])

    return "success"

@api.route("/edit")
def edit():
    global items
    # check for requiered keys
    assert has_keys(["item_name_old", "item_name_new", "item_cost_new", "item_amount_new"], request.args.keys()), "bad keys"
    assert has_item(request.args["item_name_old"]), "bad item"
    
    items.update({
            "name":request.args["item_name_new"],
            "cost":request.args["item_cost_new"],
            "amount":request.args["item_amount_new"]
        }, where("name")==request.args["item_name_old"])

    return "success", 200

@api.after_request
def save(response):
    return response