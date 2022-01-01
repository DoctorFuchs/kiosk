import argparse
import sys, os, subprocess

workdir = os.path.split(__file__)[0]
sys.path+=[os.path.join(workdir, "lib"), os.path.join(workdir, "backend")] # adds import paths

def restart(addArgs=[]):
    """Restart the run.py without upgrading and updating by default. addArgs adds arguments to run.py"""
    browser = ["-b"] if args.browser else []
    mode = ["-k"] if args.kiosk else ["-f"] if args.fullscreen else []
    sys.exit(subprocess.check_call([sys.executable, __file__]+browser+mode+addArgs))

def upgradeDependencies():   #not working with autoreload of flask
        try:
            # checks for pip module
            __import__("pip")

        except ImportError:
            # if pip wasn't found, it will install pip with ensurepip
            subprocess.check_call([sys.executable, "-m", "ensurepip"])

        finally:
            subprocess.check_call([sys.executable ,"-m" , "pip", "install", "-r", "requirements.txt", "-t", os.path.join(workdir, "lib"), "--upgrade", "--no-user"]) # --no-user => python 3.9 on Windows

def updateApplication():
    branch = "stable" # change the branch here
    # check that git is installed 
    try:
        subprocess.check_call(["git", "--version"])
    except:
        print("git isn't installed. So we can't update")
        return

    # check if this folder is a git repo
    if not os.path.isdir(os.path.join(workdir, ".git")): 
        print("This is not a git repo")
    else: 
        subprocess.check_call(f"git pull origin {branch}".split(" "))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launcher for kiosk application")
    parser.add_argument("-u", "--upgrade", help="Upgrade requirements and it's dependencys, stored in lib folder", action="store_true")
    parser.add_argument("-up", "--update", help="looks for a newer version. Only available if cloned with git (git need to be installed)", action="store_true")
    parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="Launch browser in fullscreen", action="store_true") 
    parser.add_argument("-k", "--kiosk", help="Launch browser in a 'super' fullscreen (chrome need to be installed, exit with Alt+F4)", action="store_true") 
    args = parser.parse_args()

    if args.upgrade:
        upgradeDependencies()
    
    if args.update:
        updateApplication()
        restart(["--upgrade"]) # restart with upgrade

    try:
        __import__("flask")
    except ImportError:
        upgradeDependencies()
        __import__("flask")

    # starts the server 
    import server
    server.main(args)
