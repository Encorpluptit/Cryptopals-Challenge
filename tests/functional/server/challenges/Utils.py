#
# EPITECH PROJECT, 2020
# Utils
# File description:
# The Utils class
#

import random
import base64

class Utils:
    @staticmethod
    def getRandomString(
        size=16,
        chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    ):
        return "".join(random.choice(chars) for _ in "_" * size)

    @staticmethod
    def bytesToBase64(data):
        return base64.b64encode(bytes(data)).decode()

    @staticmethod
    def base64ToBytes(data):
        return base64.b64decode(bytes(data))

    @staticmethod
    def padBlock(data, size):
        pad_size = size - len(data)
        if pad_size < 0:
            raise ValueError("cannot pad block to smaller size")
        return data + [pad_size] * (pad_size or 16)

    @staticmethod
    def unpadBlock(data):
        if not data:
            raise ValueError("Invalid padding.")

        print(data)
        pad_size = data[-1]
        payload, padding = data[:-pad_size], data[-pad_size:]

        if padding != [pad_size] * pad_size:
            raise ValueError("Invalid padding.")
        return payload

    @staticmethod
    def padToAES(data, size=16):
        if len(data) <= size:
            return Utils.padBlock(data, size)
        raise ValueError("data too long. Padding impossible.")
