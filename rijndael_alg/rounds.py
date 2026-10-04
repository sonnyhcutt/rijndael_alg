from . import gf
from .key_schedule import SBOX

DEFAULT_LOG_FILE = "aes_steps.txt"


def log_to_file(title, state, log_file=DEFAULT_LOG_FILE):
    with open(log_file, "a") as f:
        f.write(f"{title}:\n")
        f.write(state.to_string())
        f.write("\n\n")


def _trace(title, state, verbose, log_file):
    if not verbose:
        return
    state.display()
    print()
    log_to_file(title, state, log_file)


def sub_bytes(state, verbose=False, log_file=DEFAULT_LOG_FILE):
    for row in range(4):
        for col in range(4):
            state.state[row][col] = SBOX[state.state[row][col]]

    _trace("SubBytes Output", state, verbose, log_file)


def shift_rows(state, verbose=False, log_file=DEFAULT_LOG_FILE):
    # Row 0 unchanged
    # Row 1 rotated left by 1
    state.state[1] = state.state[1][1:] + state.state[1][:1]

    # Row 2 rotated left by 2
    state.state[2] = state.state[2][2:] + state.state[2][:2]

    # Row 3 rotated left by 3
    # (equivalent to right shift by 1)
    state.state[3] = state.state[3][3:] + state.state[3][:3]

    _trace("ShiftRows Output", state, verbose, log_file)


def mix_columns(state, verbose=False, log_file=DEFAULT_LOG_FILE):
    for col in range(4):
        a0 = state.state[0][col]
        a1 = state.state[1][col]
        a2 = state.state[2][col]
        a3 = state.state[3][col]

        b0 =     gf.xtime(a0) ^ (gf.xtime(a1)^a1) ^  a2               ^ a3
        b1 =     a0           ^ (gf.xtime(a1))    ^ (gf.xtime(a2)^a2) ^ a3
        b2 =     a0           ^  a1               ^ gf.xtime(a2)      ^ (gf.xtime(a3)^a3)
        b3 =     (gf.xtime(a0)^a0) ^ a1 ^ a2 ^ gf.xtime(a3)

        state.state[0][col] = b0
        state.state[1][col] = b1
        state.state[2][col] = b2
        state.state[3][col] = b3

    _trace("MixColumns Output", state, verbose, log_file)

# [ 02 03 01 01 ]
# [ 01 02 03 01 ]
# [ 01 01 02 03 ]
# [ 03 01 01 02 ]


def add_round_key(state, round_key, verbose=False, log_file=DEFAULT_LOG_FILE):
    for col in range(4):
        for row in range(4):
            state.state[row][col] ^= round_key.state[row][col]

    _trace("AddRoundKey Output", state, verbose, log_file)
    # XOR each column with column of round key
    # state[row][col] = state[row][col] XOR round_key[row][col]
