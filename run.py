import argparse
import sys, os, threading
import webbrowser as web
from time import sleep

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launcher for kiosk application")
    parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
    # At the moment in development
    # parser.add_argument("-f", "--fullscreen", help="Launch browser fullscreen (chrome need to be installed, exit with Alt+F4)", action="store_true") 
    args = parser.parse_args()

    try:
        __import__("flask")

    except ImportError:
        # retry after installing
        os.system("python3 -m pip install flask")
        sys.exit("Please restart the program, because flask is now installed")

    if args.browser:
        def startWebbrowser():
            sleep(1) # with delay, because the server is not started
            web.open_new("http://localhost:1024")

        threading.Thread(target=startWebbrowser).start()
        

    sys.path.append(__file__.replace("run.py", "backend"))
    # starts the server 
    from backend import server