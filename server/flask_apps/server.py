import threading
from flask import Flask, request, Response,  render_template
import os, subprocess, json
from flask.helpers import send_from_directory
from werkzeug.exceptions import abort
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from jinja2.exceptions import TemplateNotFound
from tinydb import Query

from .api import api, items
from server.utils.config_reader import languages, config
from server.utils.path import get_path


# flask app
app = Flask(__name__, template_folder=get_path("/server/frontend"))

@api.before_request
@app.before_request
def firewall():
    # check if flask app is secured through a firewall. If yes => it checks for the ip and look to the whitelist
    if config.firewall.active and request.remote_addr not in config.firewall.allowed_ips:
        return "You have no access to this application.", 401

# if anything is not found it return Not Found :D
@app.errorhandler(404)
def app_fallback(error):
    return Response("Not found"), 404


@app.route('/', defaults={'req_path': 'index.html'})
@app.route('/<path:req_path>')
def app_serve(req_path: str):
    # get user settings from cookies
    lang = request.cookies.get("lang", config.userinterface_defaults.language).upper() # language
    theme = request.cookies.get("theme", config.userinterface_defaults.theme).lower() # theme
    firstrun = request.cookies.get("first", "True") # first time on website for the user

    # check that lang and theme exists => if not: use default from config.ini(.template)
    if lang not in languages.keys(): lang = (config.userinterface_defaults.language).upper()
    if theme+".css" not in os.listdir(get_path("/server/frontend/css/themes")): theme = config.userinterface_defaults.theme
    try:
        if req_path.endswith(".html"):
            # render html files as templates
            return render_template(req_path, **{
                    # language
                    "lang": languages[lang],
                    "langs":languages.keys(),
                    "active_language":lang,

                    # theme
                    "themes": [x.replace(".css", "") for x in os.listdir(get_path("/server/frontend/css/themes"))],
                    "active_theme":theme,

                    # config
                    "firstrun":firstrun,
                    "contact":config.contact,

                    # database
                    "items": items,
                    "query": Query(),

                    # others
                    "active":os.path.split(req_path)[1]
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
