import os

# get absolute path of it self and it's
ABS_PATH_SELF = os.path.abspath(__file__)

# go 3 times one dir up
ABS_MODULE_PATH = ABS_PATH_SELF
for x in range(3):
    ABS_MODULE_PATH = os.path.dirname(ABS_MODULE_PATH)

def get_path(path: str) -> str:
    """get path from project dir as abs-path"""
    if path.startswith("/"):
        path = path[1:]
    return os.path.join(ABS_MODULE_PATH, path)

def createFolders():
    """create folders if they don't exist"""
    directorys = ["storages", "storages/backups", "storages/permanent_backups"]
    for directory in directorys:
        if not os.path.isdir(get_path(directory)): 
            os.mkdir(get_path(directory))
