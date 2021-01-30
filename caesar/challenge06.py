#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.debug import debug

MIN_KEY_SIZE    = 1
MAX_KEY_SIZE    = 40
SAMPLE_SIZE     = 24

def get_hamming_dist(bytes_a, bytes_b):
    assert len(bytes_a) == len(bytes_b)
    return sum(
        bin(bytes_b[i] ^ a_byte).count("1")
            for i, a_byte in enumerate(bytes_a)
    )

def get_key_sizes(bytes):
    return list(size for _, size in sorted(
        (
            get_hamming_dist(bytes[:size],
            bytes[size:size * 2]) / size,
            size
        ) for size in range(
            MIN_KEY_SIZE,
            min(MAX_KEY_SIZE + 1, len(bytes) // 2)
        )
    ))

def find_best_match(bytes):
    return min(
        (
            Utils.getEnglishnessError(
                "".join(chr(byte ^ key) for byte in bytes)
            ),
            key
        ) for key in range(0x100)
    )

def get_best_key_of_size(bytes, size):
    blocks = Utils.splitBySize(bytes, size)
    transposed_blocks = [
        [block[i] for block in blocks if len(block) > i]
            for i in range(size)
    ]
    errors, key = zip(*(
        find_best_match(block) for block in transposed_blocks
    ))

    return sum(errors) / len(errors), [*key]


def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")
    lines = Utils.readBytesFromDumpFile(argv[1])

    if len(lines) != 1:
        raise Exception("expected a single line")

    bytes = lines[0]
    sizes = get_key_sizes(bytes)

    debug("Probable sizes:", sizes, f"(taking top {SAMPLE_SIZE})")

    error, key = min(
        get_best_key_of_size(bytes, size) for size in sizes[:SAMPLE_SIZE]
    )
    if error > 2e-2:
        debug("Best key:", Utils.bytesToHex(key))
        raise Exception(f"no satisfactory match found. Lowest error: {error}")
    debug("Error:", error)
    print(Utils.bytesToHex(Utils.trimRepetitions(key)))
