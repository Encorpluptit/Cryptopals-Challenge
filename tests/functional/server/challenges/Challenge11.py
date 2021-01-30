#
# EPITECH PROJECT, 2020
# Challenge
# File description:
# The Challenge base class
#

import urllib.parse

from challenges.Challenge import Challenge

class Challenge11(Challenge):
    def __init__(self):
        super().__init__(11)

    def encode(self, data):
        payload = "".join(map(chr, data)) \
            .replace("&", "%26") \
            .replace("=", "%3D")
        data    = f"email={payload}&uid=10&role=user".encode()
        result  = self.encrypt(data)

        self.print("Encrypting", data)
        return result

    def validate(self, data):
        result = "".join(map(chr, self.decrypt(data)))

        self.print("Result was", result)
        return self.config["token"] if "role=admin" in result else b""

    def request(self, data, path):
        if path == "new_profile":
            return [self.encode(data[0])]
        if path == "validate":
            return [self.validate(data[0])]

        return [b""]
