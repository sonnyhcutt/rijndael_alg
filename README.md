# rijndael_alg

A from-scratch, educational implementation of **AES-128 (Rijndael)** encryption in
pure Python — no cryptography libraries, no external dependencies. It's built to
show how each step of the cipher actually works: Galois-field arithmetic, key
expansion, and the SubBytes / ShiftRows / MixColumns / AddRoundKey rounds.

> **⚠️ Not for production use.** This is a learning project, not an audited crypto
> library. It's pure Python (slow), not written to run in constant time (so it is
> not safe against timing side-channel attacks), and only implements single-block
> ECB-style encryption — there is no padding mode, no chaining mode (CBC/GCM/etc.),
> and no decryption path. Use [`cryptography`](https://pypi.org/project/cryptography/)
> or your platform's standard crypto library for anything real.

## What's implemented

- **`gf.py`** — GF(2⁸) polynomial arithmetic (`xtime`, `poly_mul`, `poly_mod`, `gf_mul`) used by MixColumns.
- **`state_matrix.py`** — the 4×4 byte state matrix that AES operates on, built from a 16-byte block.
- **`key_schedule.py`** — the AES-128 S-box and the Rijndael key expansion (`ExpansionKey`), producing the 11 round keys from a 16-byte cipher key.
- **`rounds.py`** — the four AES round transformations: `sub_bytes`, `shift_rows`, `mix_columns`, `add_round_key`.
- **`encrypt.py`** — wires the rounds together into the full AES-128 encryption pipeline (initial round → 9 main rounds → final round).

## Requirements

Python 3.8+. No dependencies — standard library only.

## Usage

### As a module

```python
from rijndael_alg import ExpansionKey, encrypt_block

key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
plaintext = bytes.fromhex("3243f6a8885a308d313198a2e0370734")

key_expansion = ExpansionKey.from_key_bytes(key)
key_expansion.full_expansion()

ciphertext = encrypt_block(plaintext, key_expansion)
print(ciphertext.hex())
# 3925841d02dc09fbdc118597196a0b32
```

### From the command line

```bash
# Runs the FIPS-197 Appendix B worked example by default
python -m rijndael_alg

# Or supply your own 16-byte key and plaintext, as hex
python -m rijndael_alg 000102030405060708090a0b0c0d0e0f 00112233445566778899aabbccddeeff

# Add --verbose to print and log the state matrix after every round
# (written to ./aes_steps.txt)
python -m rijndael_alg --verbose
```

## Testing

The implementation is checked against the official known-answer test vectors from
[NIST FIPS 197](https://csrc.nist.gov/pubs/fips/197/final) (Appendix B and Appendix C.1):

```bash
python -m unittest discover -s tests -v
```

## License

[MIT](LICENSE)
