import threading
from flask import Flask, request, Response,  render_template
import os, subprocess, json
from flask.helpers import send_from_directory
from werkzeug.exceptions import abort
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from jinja2.exceptions import TemplateNotFound
from tinydb import Query

from .api import api, items
from server.utils.config_reader import languages, config, get_contact_dict
from server.utils.path import get_path


# flask app
app = Flask(__name__, template_folder=get_path("/server/frontend"))

@api.before_request
@app.before_request
def firewall():
    # check if flask app is secured through a firewall. If yes => it checks for the ip and look to the whitelist 
    if config.getboolean("FIREWALL", "active") and request.remote_addr not in config.get("FIREWALL", "allowed_ips").split("\n"):
        return "You have no access to this application.", 401

# if anything is not found it return Not Found :D
@app.errorhandler(404)
def app_fallback(error):
    return Response("Not found"), 404


@app.route('/', defaults={'req_path': 'index.html'})
@app.route('/<path:req_path>')
def app_serve(req_path: str):
    # get user settings from cookies
    lang = request.cookies.get("lang", config.get("LANGUAGE", "language")).upper() # language
    theme = request.cookies.get("theme", config.get("THEME", "theme")).lower() # theme
    firstrun = request.cookies.get("first", "True") # first time on website for the user

    # check that lang and theme exists => if not: use default from config.ini(.template)
    if lang not in languages.sections(): lang = config.get("LANGUAGE", "language").upper()
    if theme+".css" not in os.listdir(get_path("/server/frontend/css/themes")): theme = config.get("THEME", "theme")
    try:
        if req_path.endswith(".html"):
            # render html files as templates
            return render_template(req_path, **{
                    # language
                    "lang": dict(languages.items(lang)),
                    "langs":languages.sections(),
                    "active_language":lang,

                    # theme
                    "themes": [x.replace(".css", "") for x in os.listdir(get_path("/server/frontend/css/themes"))],
                    "active_theme":theme,

                    # config 
                    "firstrun":firstrun,
                    "contact":get_contact_dict(),

                    # database
                    "items": items,
                    "query": Query()
            })

        else:
            # return js, css, images, icons, ... as normal file
            return send_from_directory(get_path("/server/frontend"), req_path)
            

    except TemplateNotFound or FileNotFoundError:
        return abort(404)

# create app with DispatcherMiddleware
application = DispatcherMiddleware(app, {
    '/api/shop': api
})

