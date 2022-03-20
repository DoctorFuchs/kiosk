from typing import List
from flask import Flask, request, jsonify, Response
import os
import re
from tinydb import TinyDB, where
import time

from tinydb.queries import Query

# creates folder if they don't exist
if not os.path.isdir("storages"): os.mkdir("storages")

# create item DB
items = TinyDB("storages/items.db")

# Utils
def has_item(item_name: str) -> bool:
    """check items DB for an item with item_name"""
    return items.contains(Query().name==item_name)

def has_keys(_keys: List[str], _list: List[str]) -> bool:
    """check a list of keys if they are in another list (of keys)"""
    return set(_keys).issubset(set(_list))

# Flask app
api = Flask(__name__)

# handle assertion error => raised when user input is not correct 
@api.errorhandler(AssertionError)
def failed(error):
    return "failed - "+str(error), 400

# handle not founds in api
@api.errorhandler(404)
def api_fallback(error):
    return "invalid request", 400

# get all items from items DB
@api.route("/list", methods=["GET"])
def get_all():
    return jsonify(items.all()), 200

# get information from one item
@api.route("/item", methods=["GET"])
def get():
    # check for keys
    assert has_keys(["item_name"], request.args.keys()), "bad keys"
    
    # return the item
    return jsonify(items.get(Query().name == request.args["item_name"])), 200

@api.route("/additem", methods=["POST"])
def additem():
    global items

    # check for keys
    assert has_keys(["item_name", "item_cost", "item_amount"], request.form.keys()), "bad keys"
    
    # save in variables
    item_name = request.form["item_name"]
    item_cost = request.form["item_cost"]
    item_amount = request.form["item_amount"]
    
    # check user_input
    assert not has_item(item_name), "bad item"
    assert re.match("[A-Za-z0-9+]", item_name), "bad format"
    assert re.match("[0-9+]", item_amount), "bad format"
    assert re.match("[0-9+]", item_cost), "bad format"

    # add item
    items.insert({
        "name":item_name,
        "cost":int(item_cost),
        "amount":int(item_amount)
    })

    # return response 
    return "success", 200

@api.route("/delete/<path:item_name>", methods=["DELETE"])
def delete(item_name):
    global items
    # check for keys
    assert has_item(item_name), "bad item"
    
    # check user_input
    assert re.match("[A-Za-z0-9+]", item_name), "bad format"

    # remove item from items
    items.remove(where("name") == item_name)
    
    return "success", 200
        
@api.route("/buy")
def buy():
    global items
    # check for required keys
    assert has_keys(["item_name", "item_amount"], request.args.keys()), "bad keys"
    
    # save in variables
    item_name = request.args["item_name"]
    item_amount = request.args["item_amount"]
    
    # check user input
    assert has_item(item_name), "bad item"
    assert re.match("[0-9]+", item_amount), "bad format"
    assert items.get(Query().name==item_name).get("amount")-int(item_amount)<0, "item overload"
    
    # update items
    items.update({
        "amount":items.get(Query().name==item_name).get("amount")-int(item_amount),
        }, where("name") == item_name)

    return "success"

@api.route("/edit", methods=["POST"])
def edit():
    global items
    # check for requiered keys
    assert has_keys(["item_name_old", "item_name_new", "item_cost_new", "item_amount_new"], request.form.keys()), "bad keys"
    
    # save inforamations in variables
    item_name_old = request.form["item_name_old"]
    item_name_new = request.form["item_name_new"]
    item_cost_new = request.form["item_cost_new"]
    item_amount_new = request.form["item_amount_new"]
    
    # check that item exists
    assert has_item(item_name_old), "bad item"
    if item_name_new != item_name_old:
        # if item_name changed check that item doesn't already exists
        assert not has_item(item_name_new), "item already exists"
    
    # update item
    items.update({
            "name":item_name_new,
            "cost":item_cost_new,
            "amount":item_amount_new
        }, where("name")==item_name_old)

    # send response
    return "success", 200
