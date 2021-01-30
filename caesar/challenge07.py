#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from Crypto.Cipher import AES

from caesar.Utils import Utils

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    with open(argv[1]) as file:
        lines = [line.strip() for line in file.read().splitlines() if line]
    if not lines:
        raise Exception("empty input file")
    if len(lines) != 2:
        raise Exception("expected exactly 2 lines in file")

    key     = Utils.padToAES(Utils.hexToBytes(lines[0]))
    data    = Utils.base64ToBytes(lines[1])
    cipher  = AES.new(bytes(key), AES.MODE_ECB)
    result  = [*cipher.decrypt(bytes(data))]

    print(Utils.bytesToBase64(Utils.unpadBlock(result)))
