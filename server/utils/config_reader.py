import yaml
import os
import subprocess
from .path import ABS_MODULE_PATH, get_path
from shutil import copyfile

default_config_path = get_path("/config.default.yaml")
config_path = get_path("/config.yaml")

# check that the default config exists
assert os.path.exists(default_config_path), "Default config file wasn't found: " + default_config_path

# create normal config for editing
if not os.path.exists(config_path):
    copyfile(default_config_path, config_path)

# read config
with open(default_config_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
with open(config_path, "r", encoding="utf-8") as file:
    config.update(yaml.safe_load(file) or {})
    # need to merge configs in case of updates that require new values

#read intro config
with open(get_path("server/flask_apps/intro_config.yaml"), encoding="utf-8") as file:
        introConfig = yaml.safe_load(file)

class DotDict(dict):
    """"Enables .value access for dictonarys"""
    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

config = DotDict(config)

#get version (last git commit id) and add to config
def _get_version():
    result = subprocess.run(["git", "log", "--format='%H'", "-n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        result = result.stdout.decode("utf-8").strip()
    else:
        result = "unknown"
    return result
    
config["application"]["feedback_url"] += f"?version={_get_version()}"

# read available language packs
_languages = os.listdir(get_path("/packs/language"))

# read languages
languages = {}
for lang in _languages:
    with open(get_path("/packs/language/" + lang), "r", encoding="utf-8") as file:
        languages[lang.rsplit(".", 1)[0].upper()] = yaml.safe_load(file)
languages = DotDict(languages)