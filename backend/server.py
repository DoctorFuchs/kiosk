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

    # @api.route("/firstRun") #dont now why it isn't working, should set first run to 0 when there is a request /api/firstRun?readed=1
    # def firstRunCheck():
    #     if int(request.args["readed"]) == 1:
    #         args.firstRun = 0
    #         return args.firstRun
    #     else:
    #         return str(int(args.firstRun))
    
    @api.route("/firstRun")
    def firstRunCheck():
        fR = str(int(args.firstRun))
        args.firstRun = 0
        return fR

    run_simple('localhost', 1024, application, use_reloader=config.auto_reload, use_debugger=config.debugger, use_evalex=config.evalex)