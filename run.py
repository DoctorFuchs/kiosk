import argparse
import sys, os, subprocess

os.chdir(os.path.split(__file__)[0] if os.path.split(__file__)[0] != "" else ".") 
sys.path += ["lib", "backend"] # adds import paths

def upgradeDependencies():   #not working with autoreload of flask
        try:
            # checks for pip module
            __import__("pip")

        except ImportError:
            # if pip wasn't found, it will install pip with ensurepip
            subprocess.check_call([sys.executable, "-m", "ensurepip"])

        finally:
            subprocess.check_call([sys.executable ,"-m" , "pip", "install", "-r", "requirements.txt", "-t", "lib", "--upgrade", "--no-user"]) # --no-user => python 3.9 on Windows
            sys.path.insert(1, "lib")

def updateApplication():
    branch = "stable" # change the branch here => main (unstable), stable
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
    parser = argparse.ArgumentParser(description="Launcher for kiosk application")
    parser.add_argument("-U", "--upgrade", help="Upgrade the kiosk application, only available if git repository (git needs to be installed)", action="store_true")
    parser.add_argument("-u", "--update", help="Force updating dependencies", action="store_true")
    parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
    parser.add_argument("-w", "--window", help="Launch native looking window", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="Launch window in fullscreen", action="store_true") 
    parser.add_argument("-k", "--kiosk", help="Launch chromium's kiosk mode(a 'super' fullscreen, chrom[e/ium] or edge with chromium engine needs to be installed, exit with Alt+F4)", action="store_true") 
    args = parser.parse_args()

    if args.update:
        upgradeDependencies()
    
    if args.upgrade:
        updateApplication()

    try:
        __import__("flask")
    except ImportError:
        upgradeDependencies()
        __import__("flask")

    # starts the server 
    import server
    server.main(args)
