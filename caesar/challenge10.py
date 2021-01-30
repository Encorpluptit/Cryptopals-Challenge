#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.Client import Client
from caesar.debug import debug

def decrypt_next_byte(client, suffix, size):
    padding = [0] * (size - len(suffix) - 1)
    target  = client.request(padding)[:size]

    for byte in range(0x100):
        result = client.request(padding + suffix + [byte])[:size]
        if result == target:
            return byte

def find_suffix(client):
    size    = len(client.request([]))
    suffix  = []

    for _ in "_" * size:
        byte = decrypt_next_byte(client, suffix, size)

        if byte is None:
            return Utils.unpadBlock(suffix)

        suffix += [byte]
        debug("Decrypted suffix:", Utils.bytesToHex(suffix))

    return Utils.unpadBlock(suffix)

def main(argv):
    if len(argv) != 1:
        raise Exception("no arguments expected")

    client = Client(10)
    suffix = find_suffix(client)

    if not suffix:
        raise ValueError("suffix is empty")

    print(Utils.bytesToBase64(suffix))
