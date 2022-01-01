import argparse
import sys, os, subprocess

workdir = os.path.split(__file__)[0]
sys.path+=[os.path.join(workdir, "lib"), os.path.join(workdir, "backend")] # adds import paths

def upgradeDependencies():   #not working with autoreload of flask
        try:
            # checks for pip module
            __import__("pip")

        except ImportError:
            # if pip wasn't found, it will install pip with ensurepip
            subprocess.check_call([sys.executable, "-m", "ensurepip"])

        finally:
            subprocess.check_call([sys.executable ,"-m" , "pip", "install", "-r", "requirements.txt", "-t", os.path.join(workdir, "lib"), "--upgrade", "--no-user"]) # --no-user => python 3.9 on Windows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launcher for kiosk application")
    parser.add_argument("-u", "--upgrade", help="Upgrade flask and it's dependencys, stored in lib folder", action="store_true")
    parser.add_argument("-b", "--browser", help="Launch browser while starting", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="Launch browser in fullscreen", action="store_true") 
    parser.add_argument("-k", "--kiosk", help="Launch browser in a 'super' fullscreen (chrome need to be installed, exit with Alt+F4)", action="store_true") 
    args = parser.parse_args()

    if args.upgrade:
        upgradeDependencies()

    try:
        __import__("flask")

    except ImportError:
        upgradeDependencies()
        __import__("flask")

    # starts the server 
    import server
    server.main(args)