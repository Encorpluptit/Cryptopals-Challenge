#
# EPITECH PROJECT, 2020
# Challenge
# File description:
# The Challenge base class
#

from challenges.Challenge import Challenge

class Challenge10(Challenge):
    def __init__(self):
        super().__init__(10)

    def encode(self, data):
        result = self.encrypt(bytearray([*data, *self.config["suffix"]]))

        self.print("Encrypting", *(hex(b)[2:].upper().zfill(2) for b in data))
        return result

    def request(self, data, path):
        return [b"" if path else self.encode(data[0])]
