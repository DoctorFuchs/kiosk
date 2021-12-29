from flask import Flask, request, Response, send_file
import config
from shop import shop
import os 
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

def getFrontendPath():
    """Get path to the frontend"""
    return __file__.replace("backend"+os.sep+"server.py", "frontend")+os.sep

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

run_simple('localhost', 1024, application, use_reloader=False, use_debugger=True, use_evalex=True)