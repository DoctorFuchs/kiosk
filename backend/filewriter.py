from datetime import datetime
import os

try:
    os.mkdir("logs")

except FileExistsError:
    pass


def writeToLog(message):
    """writes a message to the logs and also print the same message."""
    print(message, end="")
    log = open("logs/" + datetime.today().strftime('%D').replace("/", "-") + ".log", "a+t")
    log.write(message)
    log.close()
