import time
import shutil
import os
from tinydb import TinyDB

from server.utils.config_reader import config
from server.utils.path import get_path

last_backup = 0

def backup():
    global last_backup
    if time.time() - last_backup >= config.getfloat("APPLICATION", "backup_time_in_minutes") * 60:
        def get_oldest_backup():
            return str(min([int(file.rsplit(".", 1)[0]) for file in os.listdir(get_path("/storages/backups"))]))+".db"

        while int(config.get("APPLICATION", "max_backups")) <= len(os.listdir(get_path("/storages/backups"))):
            os.remove(get_path("/storages/backups/") + get_oldest_backup())
        timestamp = str(time.time()).split(".")[0]
        shutil.copy(get_path("/storages/items.db"), get_path(f"/storages/backups/{timestamp}.db"))
        last_backup = time.time()
        print(f"\033[95mBackup at {time.ctime()} created.\033[0m")

def listBackups():
    table_head = ["Number", "Date", "ID"]
    backups = os.listdir(get_path("/storages/backups"))
    backups = [backup.rsplit(".", 1)[0] for backup in backups]
    backups = [[backups.index(backup) + 1, time.ctime(int(backup)), backup] for backup in backups]
    row_format ="{:<10}{:>25}{:>25}"
    print(f"\033[1m{row_format.format(*table_head)}\033[0m")
    for row in backups:
        print(row_format.format(*row))
    return backups

def showBackupContent(backup):
    try:
        if not os.path.exists(f"storages/backups/{backup}.db"):
            raise FileNotFoundError 
    except FileNotFoundError:
        print("The specified backup wasn't found. Please check the id.")
        return FileNotFoundError
    items = TinyDB(get_path(f"storages/backups/{backup}.db")).all()
    items = [item.values() for item in items]
    table_head = ["Name", "Price", "Amount"]
    row_format ="{:<10}{:>25}{:>25}"
    print(f"\033[1m{row_format.format(*table_head)}\033[0m")
    for row in items:
        print(row_format.format(*row))

def restoreBackup(backup):
    if input("\033[1mAre you to totally sure? This step can't undone. For confirmation type 'yes': \033[0m") == "yes":
        try:
            shutil.copy(get_path(f"storages/backups/{backup}.db"), get_path("/storages/items.db"))
            print("\033[92mSuccessfully restored.\033[0m")
        except FileNotFoundError:
            print("The specified backup wasn't found. Please check the id.")
    else: 
        print("\033[91mRestore canceled.\033[0m")


def interactiveBackupRestore():
    print("\033[1mChoose the backup that you want to restore by typing the number and hit enter.\033[0m")
    loop = True
    while loop:   
        backups = listBackups()
        inpt = input("\033[1mType number ('n' to exit): \033[0m")
        if len(list(filter(lambda listItem: str(listItem[0]) == inpt, backups))):
            backup = list(filter(lambda listItem: str(listItem[0]) == inpt, backups))[0][-1]
            loop = False
        elif inpt == "n":
            return
        else:
            print("No match found. Try again.")
    print("\033[1mPlease review the backup content that you wanna restore. Continue with 'y'.\033[0m")
    loop = True
    while loop:   
        backups = showBackupContent(backup)
        inpt = input("\033[1mType 'y' to accept ('n' to exit): \033[0m")
        if inpt == "y":
            loop = False
        elif inpt == "n":
            return
        else:
            print("Unknown input. Try again.")
    restoreBackup(backup)