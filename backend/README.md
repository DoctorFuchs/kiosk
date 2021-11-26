# backend documentation

## api.py
connects sql to the web-app

-> api-map

[shop]/[list]<br>
[shop]/[additem]?[item_name, item_cost, item_amount]<br>
[shop]/[delete]?[item_name]<br>
[shop]/[edit]?[item_name_new, item_cost_new, item_amount_new, item_name_old]<br>

Default-port: 8080

## config.py
### Database type
You can use sqlite3 or mySql. MySQL need the mysql module. (pip3 install mysql)

### sqlite settings - for local access
Sqlite settings. The name is the name of the file. If you use :memory:, it will safe the db in ram. (No saving on program stop)

### mysql settings - to connect to database-server (this server can also hosted by third party programs)
mysql_database_host

>Host of mysql. (on your own computer localhost, else a domain or ip)

mysql_database_port

>mySQL's standard port is 3306

mysql_database_username

>your mysql username

mysql_database_password

>your mysql password

### shell configurations
modified_output is good for final viewing. Because it prints access and DB respones.

### firewall
firewall
> firewall on/off

firewall_allowed_ips
> You need 127.0.0.1, that you can access your own system. <br>
> Other ips get blocked

### debug
activate debug

## dbengine.py
excutes code at the sql connections

## filewrite.py

Write modified output to logs

## webserver.py

serves all files from /frontend to the web

