# INITIAL ROUND
# AddRoundKey(state, CipherKey)
# 9 ROUNDS
# SubBytes -> ShiftRows -> MixColumns -> AddRoundKey(state, RoundKey)
# FINAL ROUND
# SubBytes -> ShiftRows -> AddRoundKey(state, RoundKey)
# Cipher text!

from . import rounds
from .key_schedule import nr


def initial_round(state, key_expansion, verbose=False, log_file=rounds.DEFAULT_LOG_FILE):
    rounds.add_round_key(state, key_expansion.get_round_key_matrix(0), verbose, log_file)


def nine_rounds(state, key_expansion, verbose=False, log_file=rounds.DEFAULT_LOG_FILE):
    for i in range(1, nr):
        round_key = key_expansion.get_round_key_matrix(i)
        rounds.sub_bytes(state, verbose, log_file)
        rounds.shift_rows(state, verbose, log_file)
        rounds.mix_columns(state, verbose, log_file)
        rounds.add_round_key(state, round_key, verbose, log_file)


def final_round(state, key_expansion, verbose=False, log_file=rounds.DEFAULT_LOG_FILE):
    rounds.sub_bytes(state, verbose, log_file)
    rounds.shift_rows(state, verbose, log_file)
    rounds.add_round_key(state, key_expansion.get_round_key_matrix(nr), verbose, log_file)


def encrypt_block(block: bytes, key_expansion, verbose=False, log_file=rounds.DEFAULT_LOG_FILE):
    """Encrypt a single 16-byte block with an already-expanded key."""
    from .state_matrix import StateMatrix

    state = StateMatrix(block)
    initial_round(state, key_expansion, verbose, log_file)
    nine_rounds(state, key_expansion, verbose, log_file)
    final_round(state, key_expansion, verbose, log_file)
    return state.to_bytes()
