"""A from-scratch, educational implementation of AES-128 (Rijndael) in pure Python.

This package is for learning how AES works internally -- it is not
constant-time, not audited, and not intended for production use.
See README.md for details and usage.
"""

from .state_matrix import StateMatrix, pad16
from .key_schedule import ExpansionKey, Word, SBOX
from .encrypt import encrypt_block, initial_round, nine_rounds, final_round

__all__ = [
    "StateMatrix",
    "pad16",
    "ExpansionKey",
    "Word",
    "SBOX",
    "encrypt_block",
    "initial_round",
    "nine_rounds",
    "final_round",
]
