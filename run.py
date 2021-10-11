import os
import sys
import time
from threading import *
from backend import api, webserver, dbengine, config

# mySQL code snippets, that creates default database and table
CREATEKIOSK = """CREATE DATABASE if not EXISTS `kiosk`"""
USEKIOSK = """use kiosk;"""
CREATESHOP = """create table if not EXISTS shop (
    item_name text,
    item_cost double,
    item_amount int
);"""


def getLoading(pro):
    """returns a string, that make a simple loading bar. """
    com = round((pro/100)*20)
    uncom = round(20-com)
    if com-uncom != 20:
        uncom += com-uncom

    return "\r["+"-"*com+" "*uncom+"] - "+str(pro) + "%"


print("–"*25+"PREPARING SERVER"+"–"*25)

print(getLoading(0), end="")
dbengine.executeCode(code=CREATEKIOSK)
print(getLoading(33), end="")
dbengine.executeCode(code=USEKIOSK)
print(getLoading(66), end="")
dbengine.executeCode(code=CREATESHOP)
print(getLoading(100)+" - DATABASE INIT SUCCESS")

# starts webserver and api
print("–"*25+"STARTING SERVER"+"–"*26)

api_thread = Thread(target=api.main)
api_thread.start()

webserver_thread = Thread(target=webserver.main)
webserver_thread.start()

time.sleep(1)  # This wait block is needed, because on startup the servers raise sometimes errors, so you can see them

# server starts logging process
print("–"*25+"SERVER LOGGING"+"–"*27, end="")

time.sleep(1)

# prevent that the default messages from httpd.serve_forever() will printed (the new client is better :)
# but you can change it in backend/config.py)
if config.modified_output:
    print("\nMODIFIED OUTPUT ENABLED")
    sys.stderr = open(os.devnull, "w")

else:
    print("\nMODIFIED OUTPUT DISABLED", file=sys.stderr)
    sys.stdout = open(os.devnull, "w")
