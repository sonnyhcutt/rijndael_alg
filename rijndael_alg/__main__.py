"""Command-line demo for the AES-128 (Rijndael) implementation.

Usage:
    python -m rijndael_alg <hex_key> <hex_plaintext> [--verbose]

With no arguments, runs the FIPS-197 Appendix B known-answer example:
    key:        2b7e151628aed2a6abf7158809cf4f3c
    plaintext:  3243f6a8885a308d313198a2e0370734
    ciphertext: 3925841d02dc09fbdc118597196a0b32
"""
import sys

from .key_schedule import ExpansionKey
from .encrypt import encrypt_block

DEFAULT_KEY = "2b7e151628aed2a6abf7158809cf4f3c"
DEFAULT_PLAINTEXT = "3243f6a8885a308d313198a2e0370734"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    verbose = "--verbose" in argv
    argv = [a for a in argv if a != "--verbose"]

    key_hex = argv[0] if len(argv) > 0 else DEFAULT_KEY
    plaintext_hex = argv[1] if len(argv) > 1 else DEFAULT_PLAINTEXT

    key = bytes.fromhex(key_hex)
    plaintext = bytes.fromhex(plaintext_hex)

    key_expansion = ExpansionKey.from_key_bytes(key)
    key_expansion.full_expansion()

    ciphertext = encrypt_block(plaintext, key_expansion, verbose=verbose)

    print(f"Key:        {key.hex()}")
    print(f"Plaintext:  {plaintext.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")


if __name__ == "__main__":
    main()
