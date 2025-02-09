import random

def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:  
            result = (result * base) % mod
        base = (base * base) % mod  
        exp //= 2  
    return result


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

   
    for a in [2, 3, 5, 7, 11]:  
        if a >= n:
            break
        if mod_exp(a, d, n) != 1:
            return False
    return True


def generate_random_prime(start=100, end=500):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num


def the_primitive_root(p):
    if not is_prime(p):
        return None  

    phi = p - 1  

    divisors = []
    d = 2
    num = phi
    while d * d <= num:
        if num % d == 0:
            divisors.append(d)
            while num % d == 0:
                num //= d
        d += 1
    if num > 1:
        divisors.append(num)

   
    for g in range(2, p):
        if all(mod_exp(g, phi // d, p) != 1 for d in divisors):
            return g  

    return None  


def generate_keys():
    p = generate_random_prime()  
    g = the_primitive_root(p)   
    if g is None:
        raise ValueError("Failed to find a primitive root for p")

    private_key = random.randint(2, p - 2)  
    public_key = mod_exp(g, private_key, p)  

    return (p, g, public_key), private_key  


def encrypt_message(public_key, message, k):
    p, g, h = public_key
    if message >= p:
        raise ValueError("Message must be smaller than p")
    c1 = mod_exp(g, k, p) 
    c2 = (message * mod_exp(h, k, p)) % p  
    return (c1, c2)


def decrypt_message(private_key, p, ciphertext):
    c1, c2 = ciphertext
    s = mod_exp(c1, private_key, p)  
    s_inv = mod_exp(s, p-2, p)  
    message = (c2 * s_inv) % p 
    return message


public_key, private_key = generate_keys()
p, g, h = public_key

k = random.randint(2, p - 2)  
message = int(input("Enter your message here: "))  

ciphertext = encrypt_message(public_key, message, k)
decrypted_message = decrypt_message(private_key, p, ciphertext)

print("Public Key:", public_key)
print("Private Key:", private_key)
print("Original Message:", message)
print("Ciphertext:", ciphertext)
print("Decrypted Message:", decrypted_message)
