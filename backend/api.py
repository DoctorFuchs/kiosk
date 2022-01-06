from datetime import datetime
from http.server import BaseHTTPRequestHandler
from backend import dbengine
import socketserver
from backend.filewriter import writeToLog

PORT = 8080

con = dbengine.getServerConnection()
dbengine.executeCode(con, "USE kiosk")


class API(BaseHTTPRequestHandler):
    """default API, that can exec mySQL code to the server"""
    def do_GET(self):
        writeToLog("\n"+"–" * 15 + "GET REQUEST FROM " + str(self.client_address[0]) + " AT " +
                  datetime.today().strftime('%H-%M') + "–" * 16+"\n")
        writeToLog("API>>> can access: " + str(
            (self.client_address[0] in ["localhost", "127.0.0.1"])) + "\trequested path: " + self.path + "\n")

        # This code, will prevent connections from other devices (So they can't access the API)
        if self.client_address[0] not in ["localhost", "127.0.0.1"]:
            writeToLog("MySQL> permission denied \n")
            self.send_response(401, "You have no access to this api!\nPlease check, that you have permissions to use "
                                    "this api")
            self.end_headers()
            self.wfile.write(bytes("You have no access to this api!\nPlease check, that you have permissions to use "
                             "this api", "utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        # default response
        result = {"invalid request"}
        form = {}

        try:
            f = self.path.split("?")
            ff = f[1].split("&")

            for element in ff:
                i = element.split("=")
                form[i[0]] = i[1].replace("$", " ")

        except IndexError:
            pass

        if self.path.startswith("/exec"):
            try:
                writeToLog("MySQL> " + str(form.get("exec"))+"\n")
                result = str(dbengine.executeCode(con, form.get("exec"))).replace(",)", ")")

            except Exception as err:
                result = str(err)

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
                print("serving api at http://localhost:" + str(PORT))
                httpd.serve_forever()
                break  # on failure the program ends

        except OSError:
            # if port is already used
            PORT += 1
