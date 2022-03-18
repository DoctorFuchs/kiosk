from configparser import ConfigParser
import os
from server.__main__ import ABS_MODULE_PATH
from shutil import copyfile 
from server.utils.path import get_path

assert os.path.exists(ABS_MODULE_PATH + os.sep + "config.ini.default"), "config file wasn't found: "+ABS_MODULE_PATH + os.sep + "config.ini.default"

if not os.path.exists("config.ini"): copyfile("config.ini.default", "config.ini")

# config
config = ConfigParser()
config.read("config.ini.default")
config.read("config.ini")

# language packs
_languages = os.listdir(get_path("/packs/language"))

languages = ConfigParser()
for lang in _languages:
    languages.read(get_path("/packs/language/"+lang)) 

# util functions
def get_contact_dict() -> dict:
    contact_data = {}
    contact_data["admin_name"] = config.get("CONTACT", "admin_name")
    contact_data["contact_ways"] = []
    for contact_way in config.get("CONTACT", "contact_ways").split("\n"): 
        if contact_way not in config.sections(): continue
        contact_data["contact_ways"].append(dict(config[contact_way]))
            
    return contact_data