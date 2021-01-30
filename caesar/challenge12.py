#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.Client import Client
from caesar.debug import debug

def get_starting_block_diff(bytes_a, bytes_b):
    blocks_a, blocks_b = map(Utils.splitBySize, [bytes_a, bytes_b], (16,) * 2)
    return next(
        i
            for i, (a, b) in enumerate(zip(blocks_a, blocks_b))
            if a != b
    )

def find_prefix(client):
    prev_block  = client.request([])
    block       = client.request([0])
    diff        = get_starting_block_diff(prev_block, block)
    prev_diff   = diff
    size        = 1

    while diff == prev_diff:
        size += 1
        prev_block, block = block, client.request([0] * size)
        prev_diff, diff = diff, get_starting_block_diff(prev_block, block)
    return (size - 1, 16 * diff)

def decrypt_next_byte(request_fn, suffix, size):
    padding = [0] * (size - len(suffix) - 1)
    target  = request_fn(padding)[:size]

    for byte in range(0x100):
        result = request_fn(padding + suffix + [byte])[:size]

        if result == target:
            return byte

def find_suffix(request_fn):
    size    = len(request_fn([]))
    suffix  = []

    for _ in "_" * size:
        byte = decrypt_next_byte(request_fn, suffix, size)

        if byte is None:
            return Utils.unpadBlock(suffix)

        suffix += [byte]
        debug("Decrypted suffix:", Utils.bytesToHex(suffix))

    return Utils.unpadBlock(suffix)

def main(argv):
    if len(argv) != 1:
        raise Exception("no arguments expected")

    client = Client(12)
    prefix_padding, prefix_size = find_prefix(client)

    debug("Padding:", prefix_padding, "Size:", prefix_size)

    suffix = find_suffix(lambda data:
        client.request([0] * prefix_padding + data)[prefix_size:]
    )

    # if not suffix:
    #     raise ValueError("suffix is empty")

    print(Utils.bytesToBase64(suffix))
