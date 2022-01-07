from sys import stderr
import threading
from flask import Flask, request, Response, send_file
import config
from shop import shop
import os, subprocess
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


def getFrontendPath():
    """Get path to the frontend"""
    return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]+os.sep+"frontend"+os.sep

def getMimetype(filepath: str):
    """Get mimetype from file. (For example: .html => text/html) 
    This can be modified in config.py"""
    return config.mimetypes.get(filepath.split(".")[-1], config.mimetypes_default)
    

app = Flask(__name__)
api = Flask(__name__)

@shop.before_request
@api.before_request
@app.before_request
def firewall():
    if config.firewall_active and request.remote_addr not in config.firewall_allowedips: 
        return "You have no access to this application.", 401

@app.errorhandler(404)
def appFallback(error):
    return send_file("index.html")

@shop.errorhandler(404)
@api.errorhandler(404)
def apiFallback(error):
    return "invalid request"

@app.route('/', defaults={'reqPath': 'index.html'})
@app.route('/<path:reqPath>')
def appServe(reqPath):
    try:
        return send_file(getFrontendPath()+reqPath.replace("/", os.sep), mimetype=getMimetype(reqPath))
    
    except FileNotFoundError:
        return Response("", 404)


application = DispatcherMiddleware(app, {
    '/api': api,
    '/api/shop': shop
})

def main(args):
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

    run_simple('localhost', 1024, application, use_reloader=True, use_debugger=False, use_evalex=True)