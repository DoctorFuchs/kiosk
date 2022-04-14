from configparser import ConfigParser
import os
from .path import ABS_MODULE_PATH
from shutil import copyfile
from server.utils.path import get_path

# check that the default config exists
assert os.path.exists(ABS_MODULE_PATH + os.sep + "config.ini.default"), "Default config file wasn't found: " + ABS_MODULE_PATH + os.sep + "config.ini.default"

# create normal config for editing
if not os.path.exists("config.ini"):
    copyfile("config.ini.default", "config.ini")

# read config
config = ConfigParser()
config.read("config.ini")

# read available language packs
_languages = os.listdir(get_path("/packs/language"))

# read languages
languages = ConfigParser()
for lang in _languages:
    languages.read(get_path("/packs/language/" + lang))

# util functions


def get_contact_dict() -> dict:
    contact_data = {}
    contact_data["admin_name"] = config.get("CONTACT", "admin_name")
    contact_data["contact_ways"] = []
    for contact_way in (config.get("CONTACT", "contact_ways").strip()).split("\n\n"):
        contact_way = contact_way.split("\n")
        contact_way = list(map(lambda detail: detail.split("="), contact_way))

        def map_contact_way(key_value_pair):
            return list(map(lambda key_or_value: key_or_value.strip(), key_value_pair))
        contact_way = list(map(map_contact_way, contact_way))
        contact_way_dict = {}
        for key_value_pair in contact_way:
            if len(list(key_value_pair)) == 2:
                contact_way_dict[key_value_pair[0]] = key_value_pair[1]
        contact_data["contact_ways"].append(contact_way_dict)

    return contact_data
