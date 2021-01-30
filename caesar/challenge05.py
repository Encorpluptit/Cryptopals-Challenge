#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    lines = Utils.readBytesFromDumpFile(argv[1])

    if len(lines) < 2:
        raise Exception("expected at least two lines")

    key, *lines = lines

    for bytes in lines:
        padded_key = Utils.alignKeyToPadding(key, len(bytes))
        print(Utils.bytesToHex(
            [bytes[i] ^ padded_key[i] for i in range(len(bytes))]
        ))
