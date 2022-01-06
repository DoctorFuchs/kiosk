from datetime import datetime
from backend.filewriter import writeToLog
import socketserver
from http import server
import os

PORT = 80


class webserver(server.BaseHTTPRequestHandler):
    """A webserver, that streams all files from frontend to the web"""

    def do_GET(self):
        writeToLog("\n" + "–" * 15 + "GET REQUEST FROM " + str(self.client_address[0]) + " AT " +
                   datetime.today().strftime('%H-%M') + "–" * 16 + "\n")
        writeToLog("webserver>>> can access: " + str(
            (self.client_address[0] in ["localhost", "127.0.0.1"])) + "\trequested path: " + self.path + "\n")

        # This code, will prevent connections from other devices (So they can't access the Webserver)
        # if you want, that these people get an alternative website, you can do this here in this if block
        if self.client_address[0] not in ["localhost", "127.0.0.1"]:
            writeToLog("MySQL> permission denied \n")
            self.send_response(401, "You have no access to this website!\nPlease check, that you have permissions to "
                                    "use this website")
            self.end_headers()
            self.wfile.write(bytes("You have no access to this website!\nPlease check, that you have permissions to "
                                   "use this website", "utf-8"))
            return

        self.send_response(200)
        self.end_headers()

        p = str(__file__).split(os.sep)
        del p[len(p) - 1]
        p[len(p) - 1] = "frontend"
        path = str(os.sep).join(p)
        
        self.path = self.path.replace("/", os.sep)
        try:
            encoding = "utf-8"
            
            if self.path.endswith(".png"):
                encoding = "base-64"
            
            self.wfile.write(bytes("".join(open(path + self.path, "rt").readlines()), encoding))

        except (FileNotFoundError, IsADirectoryError, OSError):
            self.wfile.write(bytes("".join(open(path + os.sep+"index.html", "rt").readlines()), "utf-8"))

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super(webserver, self).end_headers()


def main():
    global PORT
    while True:
        try:
            with socketserver.TCPServer(("", PORT), webserver) as httpd:
                print("serving webserver at http://localhost:" + str(PORT))
                httpd.serve_forever()
                break

        except OSError:
            PORT += 1
