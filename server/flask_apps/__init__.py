from server.utils.config_reader import config
from server.utils import browserpath
from .server import application
from werkzeug.serving import run_simple
import threading, subprocess

def startbrowser(arguments: list):
    """Start browser with a list of arguments. """
    try:
        # call chrom[e/ium] to and start app
        subprocess.Popen([browserpath.get_default_chrome_path()]+arguments+[f"--app=http://localhost:{config.server.port}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except subprocess.CalledProcessError:
        # when error is thrown open normal webbrowser with webbrowser module
        print("\n\033[93mThe desired mode could not be started. Please check if chrom[e/ium] or edge is installed and check the log above\033[0m\n")

        # import and start webbrowser with webbrowser lib
        import webbrowser
        webbrowser.open_new(f"http://localhost:{config.server.port}")


def main(args):
    """Start client and server from args"""

    # check for arguments
    if args.window or args.kiosk:
        # default argument
        arguments = ["--start-maximized"]

        if args.kiosk:
            # set arguments to --kiosk to start browser window in a super fullscreen
            arguments = ["--kiosk"]

        elif args.fullscreen:
            # set arguments to --start-fullscreen to start browser in a normal fullscreen
            arguments = ["--start-fullscreen"]

        # start thread => because the server is not started until the browser is closed
        threading.Thread(target=lambda: startbrowser(arguments)).start()

    elif args.browser:
        # import and start webbrowser with webbrowser lib
        import webbrowser
        webbrowser.open_new(f"http://localhost:{config.server.port}")

    # run server
    run_simple('0.0.0.0',
               config.server.port,
               application,
               use_reloader=config.server.auto_reload,
               use_debugger=config.server.debugger,
               use_evalex=config.server.evalex)
