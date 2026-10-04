# 0x57 = 0101 0111 can be represented as x^6 + x^4 + x^2 + x + 1
# 0x83 = 1000 0011 can be represented as x^7 + x + 1

# 0x80 = 1000 0000
# 0x100 = 0001 0000 0000

# For Rijndael our modulo is m(x) = x^8 + x^4 + x^3 + x + 1
# In bits this is 0001 0001 1011 = 0x11B

# 1  0001     10    1   1
# ^  ^^^^     ^^    ^   ^
# |     |     |     |   |
# x^8 + x^4 + x^3 + x + 1 

RIJ_MOD = 0x11B

def xtime(a: int) -> int:
    a <<= 1           # 'multiply' by two by shifting left by one
                      # Analogus to 5 -> 50 is multiplying by 10
                      # For polynomials, this is x * a(x) = x * (x^4 + x^3 + 1) = x^5 + x^4 + x
                      # Therefore, 1001 becomes 0001 0010

    if a & 0x100:     # if we overflowed past 8 bits (0 if not 256 otherwise)
        a ^= 0x1B     # reduce using AES polynomial (0001 1011)
    return a & 0xFF   # keep 8 bits (0xFF = 1111 1111)

def poly_mul(a: int, b: int) -> int:
    result = 0
    while b:                # Loop through each bit in b
        if b & 1:           # If the bit is 1 i.e. x^n exists
            result ^= a     # Add polynomial a(x)
        a <<= 1             # Multiply a(x) by x
        b >>= 1             # Next bit in b
    return result

def poly_mod(p: int, modulus: int = RIJ_MOD) -> int:
    mod_deg = modulus.bit_length() - 1              # mod_deg is 8 (0x11B is a 9-bit number)

    while p.bit_length() - 1 >= mod_deg:            # Loop while number of bits is too large
        shift = (p.bit_length() - 1) - mod_deg      # Example: If we have 12 bits then shift by 4.
        p ^= modulus << shift                       # Cancel p's highest-degree term by XORing with
    return p                                        # the modulus aligned to that term (GF(2) subtraction)

# More details: https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/aes-development/rijndael-ammended.pdf

def gf_mul(a: int, b: int) -> int:
    product = poly_mul(a, b)      # multiply as polynomials
    reduced = poly_mod(product)   # reduce modulo AES polynomial
    return reduced

# Note. In the polynomial representation, the sum of two elements is the polynomial with coefficients
# that are given by the sum modulo 2 (i.e., 1 + 1 = 0) of the coefficients of the two terms.
# Put more simply:
# add each term of the polynomial representation
# if the coefficient is 2 then it should become 0
# if the coefficient is 1 then it should remain 1
# notice that this is just XOR (i.e. a ^ b)
