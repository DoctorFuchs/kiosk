import sqlite3
import sys
from backend import config
from backend.filewriter import writeToLog

connection = None

def createDatabaseConnection():
    global connection
    if connection != None:
        return connection

    if config.database_type == config.DBType.sqlite:
        from sqlite3 import connect
        connection = connect(config.sqlite_database_name, check_same_thread=False)

    else:
        from mysql import connector
        connection = connector.connect(
            host=config.mysql_database_host,
            port=config.mysql_database_port,
            user=config.mysql_database_username,
            passwd=config.mysql_database_password
        )


def getDatabaseConnection():
    """get a database connection"""
    return connection


def executeCode(code="") -> object:
    """executes sql-code to the default server connection
    :param code: executable code for the mysql server in mysql language """
    global connection
    cursor = connection.cursor()
    try:
        cursor.execute(code)
    
    except sqlite3.OperationalError as err:
        if err.args[0] == 'disk I/O error':
            print("\n\n>>> SORRY, PLEASE USE MYSQL OR :memory: (ONLY TEMP-SAVE) <<<\n", file=sys.__stderr__)
            exit(5)

        else:
            if config.debug:
                print(err)
            
            

    connection.commit()
    return cursor.fetchall()

