from configparser import ConfigParser
import os
from .path import ABS_MODULE_PATH, get_path
from shutil import copyfile

# check that the default config exists
assert os.path.exists(get_path("/config.ini.default")), "Default config file wasn't found: " + get_path("/config.ini.default")

# create normal config for editing
if not os.path.exists(get_path("/config.ini")):
    copyfile(get_path("/config.ini.default"), get_path("/config.ini"))

# read config
config = ConfigParser()
config.readfp(open(get_path("config.ini.default"), mode="rt", encoding="utf-8"))
config.readfp(open(get_path("config.ini"), mode="rt", encoding="utf-8"))

# read available language packs
_languages = os.listdir(get_path("/packs/language"))

# read languages
languages = ConfigParser()
for lang in _languages:
    languages.readfp(open(get_path("/packs/language/" + lang), mode="rt", encoding="utf-8"))

# utility functions
def get_contact_dict() -> dict:
    # TODO: comment this function, because it has a bad readability
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
