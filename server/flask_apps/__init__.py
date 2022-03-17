from server.utils.config_reader import config
from server.utils import browserpath
from server.flask_apps.server import application
from werkzeug.serving import run_simple

def startbrowser(arguments: list):
    try:
        subprocess.Popen([browserpath.get_default_chrome_path()]+arguments+[f"--app=http://localhost:{config.get('SERVER', 'port')}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("\n\033[93mThe desired mode could not be started. Please check if chrom[e/ium] or edge is installed.\033[0m\n")
        import webbrowser
        webbrowser.open_new(f"http://localhost:{config.get('SERVER', 'port')}")           


def main(args):
    global firstrun 
    if args.window or args.kiosk:
        arguments = ["--start-maximized"]
        if args.kiosk:
            arguments = ["--kiosk"]
        elif args.fullscreen:
            arguments = ["--start-fullscreen"]
            
        threading.Thread(target=lambda: startbrowser(arguments)).start()

    elif args.browser:
        import webbrowser
        webbrowser.open_new("http://localhost:1024")

    run_simple('localhost', 
               config.getint("SERVER", "port"), 
               application, 
               use_reloader=config.get("SERVER", "auto_reload"), 
               use_debugger=config.get("SERVER", "debugger"), 
               use_evalex=config.get("SERVER", "evalex"))