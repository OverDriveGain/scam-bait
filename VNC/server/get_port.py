# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import shutil
import sys

STARTING_PORT = 4020
PORTS_FILE = os.path.expanduser('~/opened_ports.txt')
hostName = "localhost"
serverPort = 4000

HOST_FILEPATH = os.path.expanduser('~/KeePassDB.exe')

if os.path.exists(PORTS_FILE):
    ports_file = open(PORTS_FILE, "r+")
else:
    ports_file = open(PORTS_FILE, "w")
    ports_file.write(str(STARTING_PORT))
    ports_file = open(PORTS_FILE, "r+")

# Check if first time started

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if len(self.path) > 1:
            self.get_file()
        else:
            opened_ports = ports_file.read().splitlines()
            print(opened_ports)
            last_port = opened_ports[-1]
            new_port_1 = int(last_port) + 1
            new_port_2 = int(last_port) + 2
            ports_file.write('\n' + str(new_port_2))
            ports_file.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("port", str(new_port_1))
            self.end_headers()

    def get_file(self):
        with open(HOST_FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(HOST_FILEPATH)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")