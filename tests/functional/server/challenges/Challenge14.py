#
# EPITECH PROJECT, 2020
# Challenge
# File description:
# The Challenge base class
#

import Crypto.Util.Padding as Padding

from challenges.Challenge import Challenge
from challenges.Utils import Utils

class Challenge14(Challenge):
    def __init__(self):
        super().__init__(14)

    def encryptData(self):
        ciphertext = self.encrypt(self.config["message"], self.config["iv"])

        self.print(
            "Encrypting", self.config["message"].decode(),
            "with IV", self.config["iv"].decode()
        )
        return (Padding.pad(self.config["iv"], 16)[:16], ciphertext)

    def checkPadding(self, iv, data):
        self.print(
            "Checking padding for:",
            *(hex(b)[2:].upper().zfill(2) for b in data)
        )
        self.decrypt(data, iv)

    def request(self, data, path):
        if path == "encrypt":
            return self.encryptData()
        if path == "decrypt":
            self.checkPadding(*data)
            return ["OK\n"]

        return [b""]
