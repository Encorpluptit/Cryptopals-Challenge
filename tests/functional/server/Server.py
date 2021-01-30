#!/usr/bin/env python3

#
# EPITECH PROJECT, 2020
# Server
# File description:
# The Server class
#

from http.server import BaseHTTPRequestHandler

from challenges.Utils import Utils

from challenges.Challenge10 import Challenge10
from challenges.Challenge11 import Challenge11
from challenges.Challenge12 import Challenge12
from challenges.Challenge13 import Challenge13
from challenges.Challenge14 import Challenge14

CHALLENGES = [Challenge10, Challenge11, Challenge12, Challenge13, Challenge14]

class Server(BaseHTTPRequestHandler):
    def log_message(self, *args): return

    def getCookies(self):
        return {
            k: v for k, v in (
                entry.split("=") for entry in map(
                    str.strip, self.headers.get("Cookie", "").split(";")
                ) if "=" in entry
            )
        }

    def getChallenge(self):
        prefix, *path   = self.path.split("/")[1:]
        path            = path[0] if path else None

        if not prefix.startswith("challenge"):
            return (None, None)

        challenge_id = int(prefix[9:]) - 10

        if challenge_id < 0 or challenge_id >= len(CHALLENGES):
            return (None, None)

        return (CHALLENGES[challenge_id], path)

    def getSession(self, challenge_class):
        session_id  = int(self.getCookies().get("session_id", -1))
        sessions    = self.server.sessions

        if session_id is None or session_id < 0 or session_id >= len(sessions):
            session_id  = len(sessions)
            sessions    += [{"id": session_id, "challenge": challenge_class()}]

        return session_id, sessions[session_id]

    def do_POST(self):
        self.do_request("POST")

    def do_GET(self):
        self.do_request("GET")

    def do_request(self, method):
        challenge_class, path = self.getChallenge()

        if not challenge_class:
            self.send_response(404)
            self.end_headers()
            return self.wfile.write(b"No such challenge")

        session_id, session = self.getSession(challenge_class)
        challenge = session["challenge"]
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))

        self.execChallenge(challenge, data, session_id, path)

    def execChallenge(self, challenge, data, session_id, path):
        challenge.loadConfig()

        try:
            result = challenge.request(
                [*map(Utils.base64ToBytes, data.splitlines())] or [b""],
                path
            )
        except Exception as e:
            print("Error:", e)
            return self.respond(session_id, str(e).encode(), 500)

        self.respond(
            session_id,
            "\n".join(
                line if type(line) is str else Utils.bytesToBase64(line)
                    for line in result
            ).encode()
        )

    def respond(self, session_id, data, status = 200):
        self.send_response(status)
        self.send_header("Set-Cookie", f"session_id={session_id}")
        self.end_headers()
        self.wfile.write(data)
