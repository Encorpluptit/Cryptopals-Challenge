#!/usr/bin/env python3

#
# EPITECH PROJECT, 2020
# server
# File description:
# The Server class
#

import sys
from http.server import HTTPServer

from Server import Server

IP, PORT = ("127.0.0.1", 5000)

def main(argv):
    webServer = HTTPServer((IP, PORT), Server)
    webServer.sessions = []
    print(f"Server listening on http://{IP}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt: pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(84)
