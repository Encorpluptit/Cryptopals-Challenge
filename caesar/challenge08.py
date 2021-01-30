#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils

AES_BLOCK_SIZES = (16, 24, 32)

def find_ecb_line(lines, size):
    distance, line = max(
        (
            (
                len(data) // size - len(
                    set(tuple(data[i:i + size])
                        for i in range(0, len(data), size))
                ),
                n + 1
            ) for n, data in enumerate(lines) if not len(data) % size
        ),
        default=(0, 0)
    )
    return line if distance else None

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    with open(argv[1]) as file:
        lines = [line.strip() for line in file.read().splitlines() if line]
    if not lines:
        raise Exception("empty input file")

    for size in AES_BLOCK_SIZES:
        line = find_ecb_line([*map(Utils.base64ToBytes, lines)], size)
        if line:
            return print(line)
    raise Exception("no matching line found")
