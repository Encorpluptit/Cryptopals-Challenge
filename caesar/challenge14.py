#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.Client import Client
from caesar.debug import debug

def is_valid_padding(client, iv, ciphertext):
    return client.checkPadding(iv, ciphertext) == "OK"

def flip_nth_bit(payload, n, mask=1):
    result = payload[:]
    result[n] ^= mask
    return result

def get_padding_size(client, payload):
    is_valid = False
    i = 1

    while not is_valid:
        if i == 17:
            return 16
        new_payload = flip_nth_bit(payload, -16 - i, 16)
        is_valid = client.checkPadding(new_payload[:16], new_payload[16:])
        i += 1
    return i - 2

def decrypt_last_byte(client, prev_block, block, decrypted):
    size        = len(decrypted)
    nulled_mask = [0] * (16 - size) + decrypted
    padded_mask = [0] * (16 - size) + [size + 1] * size
    nulled_prev = Utils.xorData(prev_block, nulled_mask)
    new_prev    = Utils.xorData(nulled_prev, padded_mask)

    for i in range(1, 0x100):
        if client.checkPadding(flip_nth_bit(new_prev, -size - 1, i), block):
            return i ^ (size + 1)
    raise ValueError("neither byte matched; decryption impossible")

def decrypt(client, prev_block, block, decrypted=[]):
    while len(decrypted) < 16:
        last = decrypt_last_byte(client, prev_block, block, decrypted)
        decrypted = [last] + decrypted
        debug("Decrypted byte:", last)

    debug("Decrypted block:", decrypted)
    return decrypted

def main(argv):
    if len(argv) != 1:
        raise Exception("no arguments expected")

    client              = Client(14)
    iv, ciphertext      = client.get("encrypt")
    payload             = iv + ciphertext
    blocks              = Utils.splitBySize(payload, 16)
    *pairs, last_pair   = [*zip([None] + blocks, blocks)][1:]
    padding             = get_padding_size(client, payload)

    debug("Padding byte is", padding)

    result = sum([decrypt(client, *pair) for pair in pairs], []) + \
        decrypt(client, *last_pair, [padding] * padding)[:-padding]

    if not result:
        raise ValueError("message is empty")

    print(Utils.bytesToBase64(result))
