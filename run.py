import argparse
import os
import subprocess
import sys
parser = argparse.ArgumentParser(description="Launcher for kiosk application")
parser.add_argument("-u", "--upgrade", help="Upgrade flask and it's dependencys, stored in lib folder", action="store_true")
parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
parser.add_argument("-f", "--fullscreen", help="Launch browser fullscreen (chrome need to be installed, works only with -b/--browser, exit with Alt+F4)", action="store_true")
args = parser.parse_args()

dir = os.path.split(__file__)[0]
sys.path.append(os.path.join(dir, "lib"))

def upgradeDependencys():   #not working with autoreload of flask
    try:
        import pip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
    subprocess.check_call([sys.executable ,"-m" , "pip", "install", "flask", "-t", os.path.join(dir, "lib"), "--upgrade"])
    # import pip
    # pip.main(["install", "flask", "-t", os.path.join(dir, "lib"), "--upgrade"])
    import flask
    print("\nStarting now...\n")

if args.upgrade:
    upgradeDependencys()

try:
    __import__("flask")
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


sys.path.append(os.path.join(dir, "backend"))
from backend import server
