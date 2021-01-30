#
# EPITECH PROJECT, 2020
# Client
# File description:
# The Client class for last of challenges
#

import requests

from caesar.Utils import Utils

class Client:
    def __init__(self, challenge_id, address="127.0.0.1", port=5000):
        self.url        = f"http://{address}:{port}/challenge{challenge_id}"
        self.cookie     = ""

    def request(self, byte_array, path=""):
        resp = requests.post(
            self.url + ("/" + path if path else ""),
            data=Utils.bytesToBase64(byte_array),
            headers={"Cookie": self.cookie}
        )
        self.cookie = resp.headers.get("Set-Cookie", "")

        # if not resp.content:
        #     raise ValueError("empty response")

        return Utils.base64ToBytes(resp.content.decode())

    def get(self, path=""):
        resp = requests.get(
            self.url + ("/" + path if path else ""),
            headers={"Cookie": self.cookie}
        )
        self.cookie = resp.headers.get("Set-Cookie", "")

        return [
            Utils.base64ToBytes(line.decode())
                for line in resp.content.splitlines()
        ]

    def checkPadding(self, iv, ciphertext):
        resp = requests.get(
            self.url + "/decrypt",
            data="\n".join(map(Utils.bytesToBase64, [iv, ciphertext])),
            headers={"Cookie": self.cookie}
        )
        self.cookie = resp.headers.get("Set-Cookie", "")

        return resp.status_code == 200
