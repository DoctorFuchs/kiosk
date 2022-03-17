from server.__main__ import ABS_MODULE_PATH
import os

def get_path(path) -> str:
    return ABS_MODULE_PATH + path.replace("/", os.sep)