import time
import shutil
import os
from tinydb import TinyDB

from server.utils.config_reader import config
from server.utils.path import get_path

last_backup = 0

def backup(backups_path = get_path("storages/backups"), permanent = False):
    global last_backup
    if os.path.exists(get_path("storages/items.db")):
        if time.time() - last_backup >= config.application.backup_time_in_minutes * 60:
            if not permanent:
                def get_oldest_backup():
                    return str(min([int(backup.rsplit(".", 1)[0]) for backup in os.listdir(backups_path)])) + ".db"

                while config.application.max_backups <= len(os.listdir(backups_path)):
                    os.remove(os.path.join(backups_path, get_oldest_backup()))
            timestamp = str(time.time()).split(".")[0]
            shutil.copy(get_path("/storages/items.db"),os.path.join(backups_path, f"{timestamp}.db"))
            last_backup = time.time()
            print(f"\033[95mCreated {'permanent ' if permanent else ''}backup at {time.ctime()}.\033[0m")
    else:
        print("\033[91mNo database to backup found.\033[0m")

def listBackups(backups_path):
    table_head = ["Number", "Date", "ID"]
    backups = os.listdir(backups_path)
    backups = [backup.rsplit(".", 1)[0] for backup in backups]
    backups = [[backups.index(backup) + 1, time.ctime(int(backup)), backup] for backup in backups]
    row_format ="{:<10}{:>25}{:>25}"
    print(f"\033[1m{row_format.format(*table_head)}\033[0m")
    for row in backups:
        print(row_format.format(*row))
    return backups

def showBackupContent(backup, backups_path):
    try:
        if not os.path.exists(os.path.join(backups_path, f"{backup}.db")):
            raise FileNotFoundError 
    except FileNotFoundError:
        print("The specified backup wasn't found. Please check the id or try the -p flag to access permanent backups.")
        return FileNotFoundError
    items = TinyDB(os.path.join(backups_path ,f"{backup}.db")).all()
    items = [item.values() for item in items]
    table_head = ["Name", "Price", "Amount"]
    row_format ="{:<10}{:>25}{:>25}"
    print(f"\033[1m{row_format.format(*table_head)}\033[0m")
    for row in items:
        print(row_format.format(*row))
    return items

def restoreBackup(backup_id, backups_path):
    if os.path.exists(os.path.join(backups_path ,f"{backup_id}.db")):
        if input("\033[1mAre you sure that you want to restore? Before restore a permant backup will be created. For confirmation type 'yes': \033[0m") == "yes":
            backup(get_path("storages/permanent_backups"), True)
            shutil.copy(os.path.join(backups_path ,f"{backup_id}.db"), get_path("/storages/items.db"))
            print("\033[92mSuccessfully restored.\033[0m")
        else: 
            print("\033[91mRestore canceled.\033[0m")
    else:
        print("The specified backup wasn't found. Please check the id or try the -p flag to access permanent backups.")
    return backup_id

def deleteBackup(backup, backups_path):
    if not os.path.exists(os.path.join(backups_path, f"{backup}.db")):
        print("The specified backup wasn't found. Please check the id or try the -p flag to access permanent backups.")
    else:
        if input("\033[1mAre you to totally sure? This step can't undone. For confirmation type 'yes': \033[0m") == "yes":
            os.remove(os.path.join(backups_path, f"{backup}.db"))
            print("\033[92mSuccessfully deleted.\033[0m")
        else:
            print("\033[91mDelition canceled.\033[0m")
    return backup

def interactiveBackupRestore():
    table_head = ["Symbol", "Type", "Path"]
    backups_paths = [["a", "automatic", "/storages/backups"], ["p", "permanent", "/storages/permanent_backups"]]
    row_format ="{:<10}{:<25}{:<25}"
    print("\033[1mChoose the type that you want to restore by typing the symbol and hit enter.\033[0m")
    print(f"\033[1m{row_format.format(*table_head)}\033[0m")
    for row in backups_paths:
        print(row_format.format(*row))
    loop = True
    while loop:   
        inpt = input("\033[1mType symbol to select ('n' to exit): \033[0m")
        if len(list(filter(lambda listItem: str(listItem[0]) == inpt, backups_paths))):
            backups_path = list(filter(lambda listItem: str(listItem[0]) == inpt, backups_paths))[0][-1]
            backups_path = get_path(backups_path)
            loop = False
        elif inpt == "n":
            return
        else:
            print("Unknown input. Try again.")

    print("\033[1mChoose the backup that you want to restore by typing the number and hit enter.\033[0m")
    loop = True
    while loop:   
        backups = listBackups(backups_path)
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
        backups = showBackupContent(backup, backups_path)
        inpt = input("\033[1mType 'y' to accept ('n' to exit): \033[0m")
        if inpt == "y":
            loop = False
        elif inpt == "n":
            return
        else:
            print("Unknown input. Try again.")

    restoreBackup(backup, backups_path)
