"""
RSA Algorithm - Improved Version

Improvements over the original
1- Miller-Rabin primality test (0(k log²n) vs O(sqrt(n))
2- Random large prime generation (cryptographically sound)
3- Public exponement fied to 65537 (industry standard)
4- mdinv calls extend_euclid only once (bug fix)
5- Extended encoding via UTF-8: uppercase, digits, ponctuations and unicodes
6- Robust bloc splitting using fixed byte-length chunks
7- Explicite erro handling with Python exceptions
8- No mutable global state

"""
import math
import random
from typing import Tuple, List


# ---------------------------------------------------------------------------
# 1. MODULAR ARITHMETIC
# ---------------------------------------------------------------------------

def extended_euclid(a, b):
    """
    Extended Euclidean Algorithm (iterative
    Retunns (d, x, z) such that a*x + b*z = d = gcd(a, b)

    Fix: the orignal recurisve version called extended_euclid twice inside modinv
    (once to check, once to compute). This iterative version is called only once
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, a, b = b // a, b % a, a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def modinv(a: int, m: int) -> int:
    d, x, _ = extended_euclid(a % m, m)
    if d != 1:
        raise ValueError(f"Modular inverse of {a} mod {m} does not exist (gcd={d})")
    return x % m

def _miller_rabin_round(n: int, d: int, r: int, a: int) -> bool | None:
    """Single round ouf the Miller-Rabin test for witness base a"""
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r-1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        return False
    return None


def is_prime(n: int, rounds: int = 20) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    bases = random.sample(range(2, min(n - 2, 1000)), min(rounds, n - 4))
    return all(_miller_rabin_round(n, d, r, a) for a in bases)


def gen_random_prime(bits: int = 512) -> int:
    while True:
        candidate = random.getrandbits(bits) | (1 << bits -1) | 1
        if is_prime(candidate):
            return candidate


def rsa_gen_keys(bits: int = 512) -> tuple[tuple[int, int], tuple[int, int]] | None:

    E = 65537  # standard public exponent

    while True:
        p = gen_random_prime(bits)
        q = gen_random_prime(bits)
        if p == q:
            continue
            return None
        n = p * q
        phi = (p - 1) * (q - 1)
        if math.gcd(E, phi) == 1:
            d = modinv(E, phi)
            return (n, E), (n, d)


def encode_message(message: str) -> bytes:
    """
    Encodes a text message to UTF-8 bytes.

    Improvement: the original only handled 26 lowercase letters and a space
    via a hand-built dictionary. UTF-8 covers all Unicode characters
    (accents, uppercase, digits, punctuation, emojis...).
    """
    return message.encode("utf-8")


def decode_message(data: bytes) -> str:
    """Decodes UTF-8 bytes back to a string."""
    return data.decode("utf-8")


def bytes_to_int(b: bytes) -> int:
    """Converts bytes to an integer (big-endian)."""
    return int.from_bytes(b, byteorder="big")


def int_to_bytes(n: int, length: int) -> bytes:
    """Converts an integer to a fixed-length byte string (big-endian)."""
    return n.to_bytes(length, byteorder="big")


def rsa_encrypt_block(m: int, n: int, e: int) -> int:
    """Encrypts a single integer block m with public key (n, e)."""
    if m >= n:
        raise ValueError(f"Block value ({m}) must be smaller than n ({n})")
    return pow(m, e, n)  # fast built-in modular exponentiation


def rsa_decrypt_block(c: int, n: int, d: int) -> int:
    """Decrypts a single integer block c with private key (n, d)."""
    return pow(c, d, n)


def encrypt(message: str, public_key: Tuple[int, int]) -> List[int]:
    """
    Encrypts a text message into a list of integer ciphertext blocks.

    The message is split into byte chunks of size block_size = byte_length(n) - 1,
    which guarantees every block is strictly less than n.

    Improvement: the original split was brittle (decimal string arithmetic).
    This version works directly on bytes for correctness and simplicity.
    """
    n, e = public_key
    byte_len = (n.bit_length() + 7) // 8
    block_size = byte_len - 1  # guarantees block < n

    raw = encode_message(message)
    # Zero-pad the last block to a full block_size
    padded = raw + b"\x00" * ((-len(raw)) % block_size)

    ciphertext = []
    for i in range(0, len(padded), block_size):
        block = padded[i:i + block_size]
        m = bytes_to_int(block)
        ciphertext.append(rsa_encrypt_block(m, n, e))
    return ciphertext


def decrypt(ciphertext: List[int], private_key: Tuple[int, int], original_len: int) -> str:
    """
    Decrypts a list of integer blocks and returns the original message.

    `original_len` is the byte length of the UTF-8-encoded message,
    needed to strip the zero-padding added during encryption.
    """
    n, d = private_key
    byte_len = (n.bit_length() + 7) // 8
    block_size = byte_len - 1

    plaintext = b""
    for c in ciphertext:
        m = rsa_decrypt_block(c, n, d)
        plaintext += int_to_bytes(m, block_size)

    return decode_message(plaintext[:original_len])


# ---------------------------------------------------------------------------
# 6. DEMO
# ---------------------------------------------------------------------------

def demo(message: str, bits: int = 256) -> None:
    """
    Generates keys, encrypts and decrypts a message, and prints each step.

    bits=256 is used here for speed; use bits >= 2048 in production.
    """
    print("=" * 60)
    print(f"Original message  : {message!r}")

    print(f"\n[1] Generating RSA keys ({bits}-bit primes)...")
    public_key, private_key = rsa_gen_keys(bits=bits)
    n, e = public_key
    _, d = private_key
    print(f"    n = {n}")
    print(f"    e = {e}  (standard public exponent)")
    print(f"    d = {d}  (private key — keep this secret!)")

    raw_bytes = encode_message(message)
    print(f"\n[2] UTF-8 encoding : {raw_bytes.hex()}")

    print("\n[3] Encrypting in blocks...")
    ciphertext = encrypt(message, public_key)
    print(f"    {len(ciphertext)} encrypted block(s): {ciphertext}")

    print("\n[4] Decrypting...")
    recovered = decrypt(ciphertext, private_key, len(raw_bytes))
    print(f"    Recovered message : {recovered!r}")

    print("\n[5] Verification...", end=" ")
    assert recovered == message, "FAILED: decrypted message does not match!"
    print("OK - messages are identical.")
    print("=" * 60)


if __name__ == "__main__":
    # Various examples to demonstrate the robustness of UTF-8 encoding
    demo("julie is eating bread", bits=256)
    demo("Hello, World! RSA in Python.", bits=256)
    demo("RSA works with unicode too: cafe, naive, 日本語", bits=512)
