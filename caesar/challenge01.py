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

    if len(lines) != 1:
        raise Exception("expected single line")
    print(Utils.bytesToBase64(lines[0]))
