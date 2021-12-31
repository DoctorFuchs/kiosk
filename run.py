import argparse
parser = argparse.ArgumentParser(description="Launcher for kiosk application")
parser.add_argument("-u", "--upgrade", help="Upgrade flask and it's dependencys, stored in lib folder", action="store_true")
parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
parser.add_argument("-f", "--fullscreen", help="Launch browser fullscreen (chrome need to be installed, exit with Alt+F4)", action="store_true")
args = parser.parse_args()

import sys
import subprocess
sys.path.append("./lib")

def upgradeDependencys():   #not working with autoreload of flask
    try:
        import pip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
    # subprocess.check_call([sys.executable ,"-m" , "pip", "install", "flask", "-t", "./lib", "--upgrade"])
    import pip
    pip.main(["install", "flask", "-t", "./lib", "--upgrade"])
    import flask
    print("\nStarting now...\n")

if args.upgrade:
    upgradeDependencys()

try:
    import flask
except ImportError:
    try:
        upgradeDependencys()
    except ImportError:
        print("Unable to install dependencies. Please install flask and it's dependencies manually (e.g. pip3 install flask).")
        sys.exit()

if args.browser:
    def openBrowser():
        import webbrowser 
        webbrowser.open_new("http://localhost:1024")    #Dont now why it opens two tabs sometimes???
    try:
        if args.fullscreen:
            subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "http://localhost:1024", "--kiosk"])   #Add cross-platform support
        else:
            openBrowser()
    except FileNotFoundError:
        openBrowser()


sys.path.append("./backend")
from backend import server
