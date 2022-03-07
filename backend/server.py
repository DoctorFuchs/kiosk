import threading
from flask import Flask, request, Response, send_file, render_template
import config
from languages import languages
from api import api
import os, subprocess
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from jinja2.exceptions import TemplateNotFound

firstrun = False

def getFrontendPath():
    """Get path to the frontend"""
    return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]+os.sep+"frontend"+os.sep

def getMimetype(filepath: str):
    """Get mimetype from file. (For example: .html => text/html) 
    This can be modified in config.py"""
    return config.mimetypes.get(filepath.split(".")[-1], config.mimetypes_default)
    

app = Flask(__name__)

@api.before_request
@app.before_request
def firewall():
    if config.firewall_active and request.remote_addr not in config.firewall_allowedips: 
        return "You have no access to this application.", 401

@app.errorhandler(404)
def app_fallback(error):
    return render_template("index.html")

@api.errorhandler(404)
def api_fallback(error):
    return "invalid request"

@app.route('/', defaults={'req_path': 'index.html'})
@app.route('/<path:req_path>')
def app_serve(req_path):
    lang = request.cookies.get("lang", config.default_language)
    try:
        try:
            return render_template(req_path, **{
                "lang": languages.get(lang),
                "firstrun":firstrun,
                "contact":config.contact,
                "langs":languages.keys(),
                "active_language":lang
                })
        
        except TemplateNotFound:
            return send_file(getFrontendPath()+req_path.replace("/", os.sep), mimetype=getMimetype(req_path))

    except FileNotFoundError:
        return Response("", 404)


application = DispatcherMiddleware(app, {
    '/api/shop': api
})

def main(args):
    global firstrun 
    if args.window or args.kiosk:
        import browserpath
        arguments = ["--start-maximized"]
        if args.kiosk:
            arguments = ["--kiosk"]
        elif args.fullscreen:
            arguments = ["--start-fullscreen"]

        def startbrowser():
            try:
                subprocess.Popen([browserpath.get_default_chrome_path()]+arguments+["--app=http://localhost:1024"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print("\n\033[93mThe desired mode could not be started. Please check if chrom[e/ium] or edge is installed.\033[0m\n")
                import webbrowser
                webbrowser.open_new("http://localhost:1024")

        threading.Thread(target=startbrowser).start()

    elif args.browser:
        import webbrowser
        webbrowser.open_new("http://localhost:1024")
    
    firstrun = args.firstrun

    run_simple('localhost', config.port, application, use_reloader=config.auto_reload, use_debugger=config.debugger, use_evalex=config.evalex)