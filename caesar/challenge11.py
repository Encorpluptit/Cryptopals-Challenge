#
# EPITECH PROJECT, 2020
# main
# File description:
# Main entry point
#

from caesar.Utils import Utils
from caesar.Client import Client
from caesar.debug import debug

#          [     0:16     ][     16:32    ][     32:48    ]
# block_a: email=____________&uid=10&role=
# block_b: email=__________admin@@@@@@@@@@&uid=10&role=user
# where @ = padding size (11)

def get_token(client):
    block_a = client.request(b"_" * 13, "new_profile")[:32]
    block_b = client.request(
        b"_" * 10 + b"admin" + b"\x0b" * 11,
        "new_profile"
    )[16:32]

    debug(block_a, block_b)
    return client.request(block_a + block_b, "validate")

def main(argv):
    if len(argv) != 1:
        raise Exception("no arguments expected")

    client  = Client(11)
    token   = get_token(client)

    if not token:
        raise ValueError("token is empty")

    print(Utils.bytesToBase64(token))
