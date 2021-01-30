#
# EPITECH PROJECT, 2020
# Challenge
# File description:
# The Challenge base class
#

import json

from Crypto.Cipher import AES
import Crypto.Util.Padding as Padding

from challenges.Utils import Utils

class Challenge:
    def __init__(self, id):
        self.id = id

    def loadConfig(self):
        with open("./tests/functional/server/config.json") as file:
            self.config = {
                key: val.encode()
                    for key, val in json.load(file).items()
            }

    def print(self, *args):
        print(f"[Challenge {self.id}]:", *args)

    def encrypt(self, payload, iv=None):
        key     = Padding.pad(bytearray(self.config["key"]), 16)[:32]
        cipher  = AES.new(key, AES.MODE_CBC, iv=Padding.pad(iv, 16)[:16]) \
            if iv \
            else AES.new(key, AES.MODE_ECB)

        return [*cipher.encrypt(Padding.pad(payload, 16))]

    def decrypt(self, payload, iv=None):
        key     = Padding.pad(bytearray(self.config["key"]), 16)[:32]
        cipher  = AES.new(key, AES.MODE_CBC, iv=Padding.pad(iv, 16)[:16]) \
            if iv \
            else AES.new(key, AES.MODE_ECB)

        return [*Padding.unpad(cipher.decrypt(payload), 16)]
