# Round constants: one for each of the 64 rounds.
# First 32 bits of the fractional parts of the cube roots of the first 64 primes.
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
# Initial state: the starting values of the 8 working variables (a to h).
# First 32 bits of the fractional parts of the square roots of the first 8 primes.
H0 = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]
# K and H0 are fixed constants defined in NIST FIPS 180-4
# every sha256 implementation uses exactly these values
# changing any of them results in a different non standard hash function
MASK32 = 0xFFFFFFFF
# Keeps numbers at 32 bits: x & MASK32 drops everything above bit 32.

def pad(message: bytes) -> bytes:
    msg_bit_length = len(message) * 8
    padded = message + b"\x80"
    while len(padded) % 64 != 56:
        padded += b"\x00"
    padded += msg_bit_length.to_bytes(8, "big")
    return padded
    
def rotr(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32
# example rotr(0x12345678, 8)
# step 1  x >> n  shift right the last n bits fall off  0x00123456
# step 2  x << (32 - n)  shift the same number left the fallen bits go to the far left  0x12345678000000
# step 3  step1 | step2  join the two  0x12345678123456
# step 4  step3 & MASK32  drop everything outside 32 bits  0x78123456
