#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.debug import debug

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    lines = Utils.readBytesFromDumpFile(argv[1])

    if len(lines) != 1:
        raise Exception("expected a single line")

    bytes = lines[0]
    error, key = min([
        (
            Utils.getEnglishnessError(
                "".join(chr(byte ^ key) for byte in bytes)
            ),
            key
        ) for key in range(0x100)
    ])

    debug("Error:", error)
    if error > 2e-3:
        raise Exception("no satisfying key found")
    print(Utils.bytesToHex([key]))
