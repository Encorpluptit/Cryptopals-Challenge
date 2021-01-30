#
# EPITECH PROJECT, 2020
# Challenge
# File description:
# The Challenge base class
#

from challenges.Challenge import Challenge
from challenges.Utils import Utils

class Challenge13(Challenge):
    def __init__(self):
        super().__init__(13)

    def encryptData(self, data):
        payload = "".join(chr(c) for c in data if chr(c) not in ";=").encode()
        data    = self.config["prefix"] + payload + self.config["suffix"]
        result  = self.encrypt(data, self.config["iv"])

        self.print("Encrypting", data)
        self.print(Utils.bytesToBase64(self.encrypt(b"a;admin=true;", self.config["iv"])))
        return result

    def decryptData(self, data):
        result = "".join(map(chr, self.decrypt(data, self.config["iv"])))

        self.print("Decrypting", data)
        self.print("Result was", result)
        return self.config["token"] if ";admin=true;" in result else b""

    def request(self, data, path):
        if path == "encrypt":
            return [self.encryptData(data[0])]
        if path == "decrypt":
            return [self.decryptData(data[0])]

        return [b""]
