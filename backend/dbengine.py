from backend import config
if config.database_active:
    from mysql import connector


def getServerConnection():
    """create a server connection from configuration"""
    if not config.database_active:
        return ""
    
    connection = None
    try:
        connection = connector.connect(
            host=config.database_host,
            port=config.database_port,
            user=config.database_username,
            passwd=config.database_password
        )
    except Exception as err:
        raise err

    return connection


def executeCode(connection=getServerConnection(), code="") -> object:
    """executes sql-code to the default server connection
    :param connection: changes the default connection to another mysql.connector
    :param code: executable code for the mysql server in mysql language """
    if not config.database_active:
        return ""
        
    cursor = connection.cursor()
    try:
        cursor.execute(code)
        try:
            connection.commit()

        except:
            pass

        return cursor.fetchall()

    except Exception as err:
        raise err
