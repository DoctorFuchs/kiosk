import enum


# DATABASE

class DBType(enum.Enum):
    sqlite = "sqlite3"
    mysql = "mysql"  # requires installing with pip


# general database configurations
database_type: DBType = DBType.sqlite

# sqlite settings - for local access
sqlite_database_name: str = ":memory:"  # :memory: for saving DB in ram (good for testing)

# mysql settings - to connect to database-server (this server can also hosted by third party programs)
mysql_database_host: str = "127.0.0.1"  # default: "127.0.0.1"
mysql_database_port: int = 3306  # default: 3306
mysql_database_username: str = "root"
mysql_database_password: str = "root1234"

# shell configurations
modified_output: bool = True  # default: True (False is better for debug)

# firewall
firewall: bool = True
firewall_allowed_ips: list = ["127.0.0.1"]

# debug
debug: bool = False

# PROPERTIES

class Backend(enum.Enum):
    no_access = "You have no access to this %service%!\nPlease check, that you have permissions to use this %service%"
    on_request_header = "\n" + "–" * 15 + "GET REQUEST FROM %ip_address%  AT %time%" + "–" * 16 + "\n"
    on_request = "%service%>>> can access: %canAccess% \trequested path: %path%\n"
    serving = "serving %service% at http://localhost:%port%"
    stopping = "stopping %service%"
