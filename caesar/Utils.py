#
# EPITECH PROJECT, 2020
# Utils
# File description:
# Utils class
#

import math

class Utils:
    @staticmethod
    def xorData(data_a, data_b):
        if len(data_a) != len(data_b):
            raise Exception("data sizes do not match")
        return [a ^ b for a, b in zip(data_a, data_b)]

    @staticmethod
    def splitBySize(arr, size):
        return [arr[i:i + size] for i in range(0, len(arr), size)]

    @staticmethod
    def removeDuplicates(arr):
        return [*dict.fromkeys(arr)]

    @staticmethod
    def trimRepetitions(arr):
        for size in range(1, len(arr) // 2 + 1):
            pattern = arr[:size]
            if all([
                arr[i:i + size] == pattern for i in range(0, len(arr), size)
            ]):
                return pattern
        return arr

    @staticmethod
    def alignStrToPadding(s, block_size, padding_char):
        return s.ljust(
            math.ceil(len(s) / block_size) * block_size,
            padding_char
        )

    @staticmethod
    def alignKeyToPadding(key, payload_size):
        return (key * math.ceil(payload_size / len(key)))[:payload_size]

    @staticmethod
    def getEnglishnessError(text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", "")

        if not text or any(c not in Utils.CHARS for c in text):
            return 1

        return sum(
            (
                Utils.LETTER_FREQUENCIES.get(c, 0) - text.count(c) / len(text)
            ) ** 2
                for c in Utils.CHARS
        ) / len(Utils.CHARS)

    @staticmethod
    def bytesToBase64(bytes):
        D = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        data = Utils.alignStrToPadding(
            "".join(bin(byte)[2:].zfill(8) for byte in bytes),
            6,
            "0"
        )

        return Utils.alignStrToPadding(
            "".join(D[int(data[i:i + 6], 2)] for i in range(0, len(data), 6)),
            4,
            "="
        )

    @staticmethod
    def base64ToBytes(text):
        if len(text) % 4:
            raise ValueError("base64 data must be aligned to 4 characters")
        D = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        text = text.rstrip("=")
        data = "".join(bin(D.index(c))[2:].zfill(6) for c in text)

        return [int(data[i:i + 8], 2) for i in range(0, len(data) // 8 * 8, 8)]

    @staticmethod
    def hexToBytes(text):
        if text.upper() != text:
            raise Exception("input should be in upper case")
        if len(text) & 1:
            raise Exception("input should contain an even number of characters")
        return [int(text[i:i + 2], 16) for i in range(0, len(text), 2)]

    @staticmethod
    def bytesToHex(bytes):
        return "".join(hex(byte)[2:].upper().zfill(2) for byte in bytes)

    @staticmethod
    def readBytesFromDumpFile(filepath):
        with open(filepath) as file:
            lines = [line.strip() for line in file.read().splitlines() if line]
        if not lines:
            raise Exception("empty input file")

        return [*map(Utils.hexToBytes, lines)]

    @staticmethod
    def padBlock(data, size):
        pad_size = size - len(data)
        if pad_size < 0:
            raise ValueError("cannot pad block to smaller size")
        return data + [pad_size] * pad_size

    @staticmethod
    def unpadBlock(data):
        pad_size = data[-1]
        payload, padding = data[:-pad_size], data[-pad_size:]

        return payload + padding * (padding != [pad_size] * pad_size)

    @staticmethod
    def padToAES(data):
        SIZES = (16, 24, 32)

        for size in SIZES:
            if len(data) <= size:
                return Utils.padBlock(data, size)
        raise ValueError("data too long. Padding impossible.")


with open("english_chars_frequencies.txt") as file:
    Utils.LETTER_FREQUENCIES = {
        entry[0]: float(entry[1]) for entry in (
            line.split("\t") for line in file.read().splitlines()
        )
    }
Utils.CHARS = {*map(chr, range(32, 0x7f))}
