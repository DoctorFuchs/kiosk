import argparse
import sys, os, subprocess
from server.utils.config_reader import config
from server.utils.path import ABS_MODULE_PATH

os.chdir(ABS_MODULE_PATH) # make project-dir to working dir
sys.path += ["lib"] # adds lib import path

def upgrade_dependencies():   #not working with autoreload of flask
        try:
            # checks for pip module
            __import__("pip")

        except ImportError:
            # if pip wasn't found, it will install pip with ensurepip
            subprocess.check_call([sys.executable, "-m", "ensurepip"])

        finally:
            # install
            subprocess.check_call([sys.executable ,"-m" , "pip", "install", "-r", "requirements.txt", "-t", "lib", "--upgrade", "--no-user"]) # --no-user => python 3.9 on Windows
            import site
            from importlib import reload
            reload(site)

def check_dependencies():
    with open("requirements.txt", "rt") as rfile:
        for requirement in rfile.read().split("\n"):
            __import__(requirement.strip())

def update_application():
    branch = config.get("APPLICATION", "branch") # get the branch from config
    # check that git is installed
    try:
        subprocess.check_call(["git", "--version"])

    except:
        print("\n\033[93mGit isn't installed, so updating is not available.\033[0m\n")
        return

    # check if this folder is a git repo
    if not os.path.isdir(".git"):
        print("\n\033[93mThis is not a git repo. Can't update.\033[0m\n")
    else:
        try:
            subprocess.check_call(f"git pull origin {branch}".split(" "))
            subprocess.check_call(f"git checkout {branch}".split(" "))
        except subprocess.CalledProcessError:

            print("\n\033[91mWhile trying to update the app an error occured. Please check the the log above for more information.\033[0m\n")

if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser(description="Launcher for kiosk application")
    parser.add_argument("-U", "--upgrade", help="Force updating dependencies", action="store_true")
    parser.add_argument("-u", "--update", help="Upgrade the kiosk application, only available if git repository (git needs to be installed)", action="store_true")
    parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
    parser.add_argument("-w", "--window", help="Launch native looking window", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="Launch window in fullscreen", action="store_true")
    parser.add_argument("-k", "--kiosk", help="Launch chromium's kiosk mode(a 'super' fullscreen, chrom[e/ium] or edge with chromium engine needs to be installed, exit with Alt+F4)", action="store_true")
    args = parser.parse_args()

    # check for arguments
    if args.upgrade:
        upgrade_dependencies()

    if args.update:
        update_application()

    # check dependencies and install if required
    try:
        check_dependencies()

    except ImportError:
        upgrade_dependencies()
        check_dependencies()

    # starts the server
    from server import flask_apps
    flask_apps.main(args)
