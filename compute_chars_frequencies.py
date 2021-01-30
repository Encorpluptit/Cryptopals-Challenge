#!/usr/bin/env python3

#
# EPITECH PROJECT, 2020
# compute_chars_frequencies
# File description:
# A utility script to compute char frequencies from a text
#

import sys

def normalize_text(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def main(argv):
    if len(argv) != 2:
        raise Exception("expected one argument")

    with open(argv[1]) as file:
        text = normalize_text(file.read())

    frequencies = sorted([
        (text.count(c) / len(text), c) for c in set(text)
    ])[::-1]

    print(*(
        ["{}\t{:.8f}".format(c, round(freq, 8)) for freq, c in frequencies]
    ), sep="\n")

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(84)
