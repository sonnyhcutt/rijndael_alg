"""Known-answer tests against the official FIPS-197 AES-128 test vectors.

Reference: NIST FIPS 197, Appendix B and Appendix C.1
https://csrc.nist.gov/pubs/fips/197/final
"""
import unittest

from rijndael_alg.key_schedule import ExpansionKey
from rijndael_alg.encrypt import encrypt_block


class TestFips197KnownAnswers(unittest.TestCase):
    def _run(self, key_hex, plaintext_hex, expected_ciphertext_hex):
        key = bytes.fromhex(key_hex)
        plaintext = bytes.fromhex(plaintext_hex)

        key_expansion = ExpansionKey.from_key_bytes(key)
        key_expansion.full_expansion()

        ciphertext = encrypt_block(plaintext, key_expansion)
        self.assertEqual(ciphertext.hex(), expected_ciphertext_hex)

    def test_fips197_appendix_b(self):
        # FIPS-197 Appendix B worked example.
        self._run(
            key_hex="2b7e151628aed2a6abf7158809cf4f3c",
            plaintext_hex="3243f6a8885a308d313198a2e0370734",
            expected_ciphertext_hex="3925841d02dc09fbdc118597196a0b32",
        )

    def test_fips197_appendix_c1(self):
        # FIPS-197 Appendix C.1 (AES-128).
        self._run(
            key_hex="000102030405060708090a0b0c0d0e0f",
            plaintext_hex="00112233445566778899aabbccddeeff",
            expected_ciphertext_hex="69c4e0d86a7b0430d8cdb78070b4c55a",
        )

    def test_all_zero_key_and_plaintext(self):
        # Common sanity-check vector used across AES test suites.
        self._run(
            key_hex="00000000000000000000000000000000",
            plaintext_hex="00000000000000000000000000000000",
            expected_ciphertext_hex="66e94bd4ef8a2c3b884cfa59ca342b2e",
        )


if __name__ == "__main__":
    unittest.main()
