from datetime import datetime
from backend.filewriter import writeToLog
from backend import config
import socketserver
from http import server
import os
import base64
import sys

PORT = 80

def getFrontendPath() -> str:
    p = str(__file__).split(os.sep)
    del p[len(p) - 1]
    p[len(p) - 1] = "frontend"
    return str(os.sep).join(p)

class Webserver(server.SimpleHTTPRequestHandler):
    """A webserver, that streams all files from frontend to the web"""

    def do_GET(self):
        writeToLog(
            config.Backend.on_request_header.value
                .replace("%service%", "WEBSERVER")
                .replace("%ip_address%", str(self.client_address[0]))
                .replace("%time%", datetime.today().strftime('%H-%M'))
        )

        writeToLog(
            config.Backend.on_request.value
                .replace("%service%", "WEBSERVER")
                .replace("%canAccess%", str(self.client_address[0] in ["localhost", "127.0.0.1"]))
                .replace("%path%", self.path)
        )

        # This code, will prevent connections from other devices (So they can't access the Webserver)
        # if you want, that these people get an alternative website, you can do this here in this if block
        if self.client_address[0] not in config.firewall_allowed_ips and config.firewall:
            self.send_response(401,
                               config.Backend.no_access.value
                               .replace("%service%", "WEBSERVER"))
            self.end_headers()

            self.wfile.write(bytes(
                config.Backend.no_access.value
                    .replace("%service%", "WEBSERVER"),
                "utf-8")
            )
            return

        self.send_response(200)
        if self.path.endswith(".png"):
            self.send_header("Content-type", "image/png")
        self.end_headers()
        #self.wfile = open("test.txt", "w+b")
        path = getFrontendPath()

        self.path = self.path.replace("/", os.sep)
        try:
            self.wfile.write(open(path+self.path, "rb").read())

        except (FileNotFoundError, IsADirectoryError, OSError):
            self.wfile.write(open(path + os.sep + "index.html", "rb").read())

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super(Webserver, self).end_headers()


def main():
    """Run a TCPServer from Webserver class"""
    global PORT
    # checks forever, for a free port
    while True:
        try:
            with socketserver.TCPServer(("", PORT), Webserver) as httpd:
                print(
                    config.Backend.serving.value
                        .replace("%service%", "WEBSERVER")
                        .replace("%port%", str(PORT))
                )
                try:
                    httpd.serve_forever()
                
                except KeyboardInterrupt:
                    httpd.server_close()
                    print(config.Backend.stopping.value.replace("%service%", "WEBSERVER"))

                    print(config.Backend.stopping.value.replace("%service%", "WEBSERVER"), file=sys.stderr)

                break

        except OSError:
            PORT += 1
