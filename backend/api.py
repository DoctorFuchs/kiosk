from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from backend import dbengine
import socketserver
from backend.webserver import getFrontendPath
from backend.filewriter import writeToLog
from backend import config
import sys

PORT = 8080

con = dbengine.getDatabaseConnection()


class API(SimpleHTTPRequestHandler):
    """default API, that can exec mySQL code to the server"""
    def do_GET(self):
        writeToLog(
            config.Backend.on_request_header.value
                .replace("%service%", "API")
                .replace("%ip_address%", str(self.client_address[0]))
                .replace("%time%", datetime.today().strftime('%H-%M'))
        )
        writeToLog(
            config.Backend.on_request.value
                .replace("%service%", "API")
                .replace("%canAccess%", str(self.client_address[0] in ["localhost", "127.0.0.1"]))
                .replace("%path%", self.path)
        )

        # This code, will prevent connections from other devices (So they can't access the API)
        if self.client_address[0] not in config.firewall_allowed_ips and config.firewall:
            self.send_response(401, config.Backend.no_access.value
                               .replace("%service%", "API"))
            self.end_headers()
            self.wfile.write(bytes(config.Backend.no_access.value
                                   .replace("%service%", "API"), "utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        form = {}

        try:
            f = self.path.split("?")
            ff = f[1].split("&")

            for element in ff:
                i = element.split("=")
                form[i[0]] = i[1]\
                    .replace("%20", " ")\
                    .replace("%27", "'")

        except IndexError:
            pass

        code = ""
        result = ["invalid request"]

        if self.path.startswith("/shop/list"):
            code = "select * from shop"

        elif self.path.startswith("/shop/additem"):
            code = f"insert into shop(item_name, item_cost, item_amount)\nVALUES ('{form.get('item_name')}', {form.get('item_cost')}, {form.get('item_amount')})"

        elif self.path.startswith("/shop/delete"):
            code = f"delete from shop\nWHERE item_name='{form.get('item_name')}'"

        elif self.path.startswith("/shop/edit"):
            code = f"""update shop\nset item_name='{form.get('item_name_new')}',\n\titem_cost={form.get('item_cost_new')},\n\titem_amount={form.get('item_amount_new')}\nwhere item_name='{form.get('item_name_old')}'"""

        if code != "":
            try:
                writeToLog("DATABASE > " + code+"\n")
                result = str(dbengine.executeCode(code)).replace(",)", "]").replace(")", "]").replace("(", "[")

            except Exception as err:
                result = err
        
        if str(result) == "None":
            result = []

        writeToLog(str(result)+"\n")
        self.wfile.write(str(result).encode("utf-8"))

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super(API, self).end_headers()


def main():
    """Run a TCPServer from API class"""
    global PORT
    while True:
        try:
            with socketserver.TCPServer(("", PORT), API) as httpd:
                print(
                    config.Backend.serving.value
                        .replace("%service%", "API")
                        .replace("%port%", str(PORT))
                )
                open(getFrontendPath()+"/js/port.js", "w+t").write("var API = "+str(PORT))
                try:
                    httpd.serve_forever() 
                
                except KeyboardInterrupt:
                    httpd.server_close()
                    print(config.Backend.stopping.value
                        .replace("%service%", "API"))

                    print(config.Backend.stopping.value
                        .replace("%service%", "API"), file=sys.stderr)

                break  # on failure the program ends (or keyboard interrupt)

        except OSError:
            # if port is already used
            PORT += 1
