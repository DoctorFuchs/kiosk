import threading
from flask import Flask, request, Response, send_file, render_template
import os, subprocess, json
from flask.helpers import send_from_directory
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from jinja2.exceptions import TemplateNotFound
from tinydb import Query

from .api import api, items
from server.utils.config_reader import languages, config, get_contact_dict
from server.utils.path import get_path

app = Flask(__name__, template_folder=get_path("/server/frontend"))

@api.before_request
@app.before_request
def firewall():
    if config.getboolean("FIREWALL", "active") and request.remote_addr not in config.get("FIREWALL", "allowed_ips"):
        return "You have no access to this application.", 401

@app.errorhandler(404)
def app_fallback(error):
    return Response("Not found"), 404

@app.route('/', defaults={'req_path': 'index.html'})
@app.route('/<path:req_path>')
def app_serve(req_path: str):
    lang = request.cookies.get("lang", config.get("LANGUAGE", "language")).upper()
    theme = request.cookies.get("theme", config.get("THEME", "theme")).lower()
    firstrun = request.cookies.get("first", "True")
    
    print(theme)

    if lang not in languages.sections(): lang = config.get("LANGUAGE", "language").upper()
    if theme+".css" not in os.listdir(get_path("/server/frontend/css/themes")): theme = config.get("THEME", "theme")
    try:
        if req_path.endswith(".html"):
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
            return send_from_directory(get_path("/server/frontend"), req_path)
            

    except TemplateNotFound or FileNotFoundError:
        return Response("", 404)


application = DispatcherMiddleware(app, {
    '/api/shop': api
})

