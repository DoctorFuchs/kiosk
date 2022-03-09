from flask import Flask, request
import os
import re
import pickle

# create default variables
storageDir = __file__.replace(f"backend{os.sep}api.py", "storages")
savefilePath = storageDir + os.sep + "shop"
items = []

# creates file and folder if they don't exist
if not os.path.isdir(storageDir): os.mkdir(__file__.replace(f"backend{os.sep}api.py", "storages"))
if not os.path.isfile(savefilePath): open(savefilePath, "w+b").close()

savefile = open(savefilePath, "r+b")

try:
    items = pickle.load(savefile) 

except EOFError: 
    pass

# Utils
def hasItem(l: list, itemName: str, delete: bool=False):
    for item in range(len(l)):
        if itemName == l[item][0]:
            if delete: del l[item]
            return True, item

    return False, len(l)+1

# Flask app
api = Flask(__name__)

@api.route("/list")
def get():
    sort = request.args.get("sort", "")
    revert = request.args.get("revert", "false")

    def take(elem):
        if sort == "cost":
            ind = 1
        elif sort == "amount":
            ind = 2
        else:
            ind = 0
        return elem[ind]

    local = items.copy()
    local.sort(key=take, reverse=True if revert == "true" else False)
    return str(local)

@api.route("/additem")
def additem():
    global items
    # check for requiered keys
    if not set(["item_name", "item_cost", "item_amount"]).issubset(set(request.args.keys())): return "failed"   
    if not hasItem(items, request.args["item_name"])[0] and re.match("[A-Za-z0-9+]", request.args["item_name"]) and re.match("[0-9+]", request.args["item_amount"]) and re.match("[0-9+]", request.args["item_amount"]):
        items.append([request.args["item_name"], request.args["item_cost"], request.args["item_amount"]])
        return "success"
    
    return "failed"

@api.route("/delete")
def delete():
    global items
    # check for requiered keys
    if not set(["item_name"]).issubset(set(request.args.keys())): return "failed"   
    return ("success" if hasItem(items, request.args["item_name"], delete=True)[0] else "failed")
        

@api.route("/buy")
def buy():
    global items
    # check for required keys
    if not set(["item_name", "item_amount"]).issubset(set(request.args.keys())): return "failed"   
    if not hasItem(items, request.args["item_name"])[0] or not re.match("[0-9]+", request.args["item_amount"]):
        return "failed-format check failed"
    else:
        items[hasItem(items, request.args["item_name"])[1]][2] = str(int(items[hasItem(items, request.args["item_name"])[1]][2]) - int(request.args["item_amount"]))
        if int(items[hasItem(items, request.args["item_name"])[1]][2]) <= 0:
            del items[hasItem(items, request.args["item_name"])[1]]

    return "success"

@api.route("/edit")
def edit():
    global items
    # check for requiered keys
    if not set(["item_name_old", "item_name_new", "item_cost_new", "item_amount_new"]).issubset(set(request.args.keys())): return "failed" 
    if hasItem(items, request.args["item_name_old"])[0]:
        items[hasItem(items, request.args["item_name_old"])[1]] = [request.args["item_name_new"], request.args["item_cost_new"], request.args["item_amount_new"]]
        return "success"
    else:
        return "failed"

@api.after_request
def save(response):
    global items, savefile
    pickle.dump(items, savefile)
    # reopen savefile to save it
    savefile.close()
    savefile = open(savefilePath, savefile.mode)
    return response
