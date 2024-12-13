import random
import os
from math import gcd

def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_keys(bit_length=256):
    p = random.getrandbits(bit_length)
    while not is_prime(p):
        p = random.getrandbits(bit_length)

    g = random.randint(2, p - 2)
    x = random.randint(1, p - 2)
    h = pow(g, x, p)

    return (p, g, h), x

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def int_to_text(number):
    try:
        return number.to_bytes((number.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    except ValueError:
        return "Decryption failed (invalid data)."

def encrypt(p, g, h, message):
    plaintext = text_to_int(message)
    if plaintext >= p:
        raise ValueError("The message is too long for the chosen prime modulus. Use a larger prime.")

    k = random.randint(1, p - 2)
    c1 = pow(g, k, p)
    c2 = (plaintext * pow(h, k, p)) % p
    return c1, c2

def decrypt(p, x, c1, c2):
    s = pow(c1, x, p)
    if s == 0:
        raise ValueError("Decryption error: computed shared secret (s) is zero.")
    s_inv = modular_inverse(s, p)
    plaintext = (c2 * s_inv) % p
    return int_to_text(plaintext)

if __name__ == "__main__":
    print("Welcome to ElGamal Encryption/Decryption")
    print("1. Generate keys")
    print("2. Encrypt a message")
    print("3. Decrypt a message")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        print("\nKey Generation")
        bit_length = int(input("Enter the bit length for the prime number, example (256, 512, 1024): "))
        public_key, private_key = generate_keys(bit_length)
        print(f"Public Key: p = {public_key[0]}, g = {public_key[1]}, h = {public_key[2]}")
        print(f"Private Key: x = {private_key}")

    elif choice == "2":
        print("\nEncryption")
        p = int(input("Enter the prime number p: "))
        g = int(input("Enter the generator g: "))
        h = int(input("Enter the public key component h: "))
        message = input("Enter the secret message: ")
        try:
            c1, c2 = encrypt(p, g, h, message)
            print(f"Ciphertext: c1 = {c1}, c2 = {c2}")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == "3":
        print("\nDecryption")
        p = int(input("Enter the prime number p: "))
        x = int(input("Enter the private key x: "))
        c1 = int(input("Enter the ciphertext component c1: "))
        c2 = int(input("Enter the ciphertext component c2: "))
        try:
            message = decrypt(p, x, c1, c2)
            print(f"Decrypted message: {message}")
        except ValueError as e:
            print(f"Error: {e}")

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")