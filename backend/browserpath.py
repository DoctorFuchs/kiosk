# this file is part of the flaskwebgui 

import os
import sys
import subprocess as sps

# UTILS

def find_chrome_mac():

    chrome_names = ['Google Chrome', 'Chromium']

    for chrome_name in chrome_names:
        default_dir = r'/Applications/{}.app/Contents/MacOS/{}'.format(chrome_name, chrome_name)
        if os.path.exists(default_dir):
            return default_dir

        # use mdfind ci to locate Chrome in alternate locations and return the first one
        name = '{}.app'.format(chrome_name)
        alternate_dirs = [x for x in sps.check_output(["mdfind", name]).decode().split('\n') if x.endswith(name)] 
        if len(alternate_dirs):
            return alternate_dirs[0] + '/Contents/MacOS/{}'.format(chrome_name)

    return None


def find_chrome_linux():
    try:
        import whichcraft as wch
    except Exception as e:
        raise Exception("whichcraft module is not installed/found  \
                            please fill browser_path parameter or install whichcraft!") from e

    chrome_names = ['chromium-browser',
                    'chromium',
                    'google-chrome',
                    'google-chrome-stable']

    for name in chrome_names:
        chrome = wch.which(name)
        if chrome is not None:
            return chrome
    return None



def find_chrome_win():
    #using edge by default since it's build on chromium
    edge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    import winreg as reg
    reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'

    chrome_path = None
    last_exception = None

    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ)
            chrome_path = reg.QueryValue(reg_key, None)
            reg_key.Close()
        except WindowsError as e:
            last_exception = e
        else:
            if chrome_path and len(chrome_path) > 0:
                break

    # Only log some debug info if we failed completely to find chrome
    if not chrome_path:
        return edge_path

    return chrome_path


def get_default_chrome_path():
    """
        Credits for get_instance_path, find_chrome_mac, find_chrome_linux, find_chrome_win funcs
        got from: https://github.com/ChrisKnott/Eel/blob/master/eel/chrome.py
    """
    if sys.platform in ['win32', 'win64']:
        return find_chrome_win()
    elif sys.platform in ['darwin']:
        return find_chrome_mac()
    elif sys.platform.startswith('linux'):
        return find_chrome_linux()

