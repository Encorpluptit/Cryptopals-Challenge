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
    prev_block  = client.request([], "encrypt")
    block       = client.request([0], "encrypt")
    diff        = get_starting_block_diff(prev_block, block)
    prev_diff   = diff
    size        = 1

    while diff == prev_diff:
        size += 1
        prev_block, block = block, client.request([0] * size, "encrypt")
        prev_diff, diff = diff, get_starting_block_diff(prev_block, block)

    return (size - 1, 16 * diff)

def set_admin_role(client, prefix_padding, prefix_size):
    hash = client.request(
        [0] * prefix_padding + [*(b"\1" * 16 + b":admin<true:")],
        "encrypt"
    )

    hash[prefix_size]       ^= 1
    hash[prefix_size + 6]   ^= 1
    hash[prefix_size + 11]  ^= 1

    return client.request(hash, "decrypt")

def main(argv):
    if len(argv) != 1:
        raise Exception("no arguments expected")

    client = Client(13)
    prefix_padding, prefix_size = find_prefix(client)

    debug("Padding:", prefix_padding, "Size:", prefix_size)

    token = set_admin_role(client, prefix_padding, prefix_size)

    if not token:
        raise ValueError("token is empty")

    print(Utils.bytesToBase64(token))
