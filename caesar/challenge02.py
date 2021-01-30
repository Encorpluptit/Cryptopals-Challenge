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

    if len(lines) != 2:
        raise Exception("expected exactly two lines")
    if len(lines[0]) != len(lines[1]):
        raise Exception("line sizes do not match")

    print(Utils.bytesToHex(Utils.xorData(*lines)))
