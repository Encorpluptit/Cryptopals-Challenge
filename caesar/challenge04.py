#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.debug import debug

def find_best_line(lines):
    return min([
        (
            *min([
                (
                    Utils.getEnglishnessError(
                        "".join(chr(byte ^ key) for byte in bytes)
                    ),
                    key
                ) for key in range(0x100)
            ]),
            i + 1
        ) for i, bytes in enumerate(lines)
    ])

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    error, key, num = find_best_line(Utils.readBytesFromDumpFile(argv[1]))

    debug("Error:", error)
    if error > 2e-3:
        raise Exception("no satisfying key found")
    print(num, Utils.bytesToHex([key]))
