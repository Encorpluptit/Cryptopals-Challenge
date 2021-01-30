#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from Crypto.Cipher import AES

from caesar.Utils import Utils

KEY_SIZES   = (16, 24, 32)
BLOCK_SIZE  = 16

def decrypt(key, iv, data):
    key_size = len(key)

    if key_size not in KEY_SIZES:
        raise ValueError("invalid key size")
    if len(iv) != BLOCK_SIZE:
        raise ValueError("invalid IV size")

    pad_size    = (BLOCK_SIZE - len(data) % BLOCK_SIZE) % BLOCK_SIZE
    blocks      = Utils.splitBySize(data + [pad_size] * pad_size, BLOCK_SIZE)
    cipher      = AES.new(bytes(key), AES.MODE_ECB)

    return Utils.unpadBlock([
        item for sublist in (
            Utils.xorData([*cipher.decrypt(bytes(block))], prev)
                for block, prev in zip(blocks, [iv] + blocks)
        ) for item in sublist
    ])

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    with open(argv[1]) as file:
        lines = [line.strip() for line in file.read().splitlines() if line]
    if not lines:
        raise Exception("empty input file")
    if len(lines) != 3:
        raise Exception("expected 3 lines")

    key, iv, data = *map(Utils.hexToBytes, lines[:2]), \
        Utils.base64ToBytes(lines[2])

    print(Utils.bytesToBase64(decrypt(key, iv, data)))
