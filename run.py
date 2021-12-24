import sys
try:
    import flask

except ImportError:
    print("YOU NEED TO INSTALL FLASK: \npip3 install flask")
    sys.exit()

sys.path.append(__file__.replace("run.py", "backend"))
from backend import server
