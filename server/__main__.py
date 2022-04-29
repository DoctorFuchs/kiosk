import argparse
import sys, os, subprocess, signal
from server.utils.path import get_path, createFolders

os.chdir(get_path("/")) # make project-dir to working dir
sys.path += ["lib"] # adds lib import path
createFolders() # create folders if they don't exist

def upgrade_dependencies():   # not working with autoreload of flask
    try:
        # checks for pip module
        __import__("pip")

    except ImportError:
        # if pip wasn't found, it will install pip with ensurepip
        subprocess.check_call([sys.executable, "-m", "ensurepip"])

    finally:
        # install
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-t", "lib", "--upgrade", "--no-user"])  # --no-user => python 3.9 on Windows

        except subprocess.CalledProcessError:
            print("\n\033[91mWhile trying to install the dependencies an error occured. Please check the the log above for more information.\033[0m\n")
            sys.exit("\033[91mStartup failed.\033[0m")

        import site
        from importlib import reload
        reload(site)

def check_dependencies():
    with open("requirements.txt", "rt") as rfile:
        for requirement in rfile.read().split("\n"):
            requirement = "yaml" if requirement == "pyyaml" else requirement
            __import__(requirement.strip())

def update_application():
    from server.utils.config_reader import config
    branch = config.application.update_branch # get the branch from config
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
    parser = argparse.ArgumentParser(prog="server", description="Launcher for kiosk application", add_help=False)
    parser.add_argument("-h", "--help", help="show this help message and exit", action="store_true")
    parser.add_argument("-U", "--upgrade", help="force updating dependencies", action="store_true")
    parser.add_argument("-u", "--update", help="upgrade the kiosk application, only available if git repository (git needs to be installed)", action="store_true")
    parser.add_argument("-b", "--browser", help="launch browser while starting", action="store_true")
    parser.add_argument("-w", "--window", help="launch native looking window", action="store_true")
    parser.add_argument("-f", "--fullscreen", help="launch window in fullscreen", action="store_true")
    parser.add_argument("-k", "--kiosk", help="launch chromium's kiosk mode(a 'super' fullscreen, chrom[e/ium] or edge with chromium engine needs to be installed, exit with Alt+F4)", action="store_true")
    subparsers = parser.add_subparsers(title="Tools", dest="tool")
    backupManager = subparsers.add_parser(name="backup", description="manage database backups")
    backupGroup = backupManager.add_mutually_exclusive_group()
    backupGroup.add_argument("-i", "--interactive", help="restore backup interactively", action="store_true")
    backupGroup.add_argument("-B", "--backup", help="create a backup now", action="store_true")
    backupManager.add_argument("-p", "--permanent", help="access permanent backups (use with another option)", action="store_true")
    backupGroup.add_argument("-l", "--list", help="show list of all backups with date, time and id", action="store_true")
    backupGroup.add_argument("-s", "--show", help="view content of a backup", action="store")
    backupGroup.add_argument("-r", "--restore", help="restore with id", action="store")
    backupGroup.add_argument("-d", "--delete", help="delete backup forever", action="store")
    args = parser.parse_args()

    if args.help:
        # print main help
        print(parser.format_help())
        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        # get all subparsers and print help
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print(f"\033[1m{choice} help\033[0m")
                print(subparser.format_help())
        sys.exit()

    # check if backup subparser is active
    if args.tool == "backup":
        from server.utils.backup import *

        # catch ctrl + c to prevent error logs
        def exit(*args):
            print("")
            sys.exit(0)
        signal.signal(signal.SIGINT, exit)

        if args.permanent:
            backups_path = get_path("/storages/permanent_backups")
        else:
            backups_path = get_path("/storages/backups")

        if args.interactive:
            interactiveBackupRestore()
        elif args.backup:
            backup(backups_path, args.permanent)
        elif args.list:
            listBackups(backups_path)
        elif args.show:
            showBackupContent(args.show, backups_path)
        elif args.restore:
            restoreBackup(args.restore, backups_path)
        elif args.delete:
            deleteBackup(args.delete, backups_path)
        else:
            interactiveBackupRestore()
        sys.exit(0)

    # check dependencies and install if required
    try:
        check_dependencies()
    except ImportError:
        upgrade_dependencies()

    # check for arguments
    if args.upgrade:
        upgrade_dependencies()

    if args.update:
        update_application()

    # starts the server
    from server import flask_apps
    flask_apps.main(args)
