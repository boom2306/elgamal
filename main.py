from random import randint
from math import pow

def gcd(a, b):
  while b != 0:
    a, b = b, a % b
  return a

def power(x, y, p):
  res = 1
  x = x % p
  while y > 0:
    if y & 1:
      res = (res * x) % p
    y = y >> 1
    x = (x * x) % p
  return res

def key_gen(p):
  g = 2
  while power(g, p-1, p) != 1:
    g = g + 1

  x = randint(2, p-2)

  h = power(g, x, p)

  return g, h, x

def encrypt(m, g, h, p):
  k = randint(2, p-2)

  c1 = power(g, k, p)

  c2 = (m * power(h, k, p)) % p

  return c1, c2

def decrypt(c1, c2, x, p):
  s = power(c1, x, p)

  s_inv = power(s, p-2, p)

  m = (c2 * s_inv) % p

  return m

p = 22
g, h, x = key_gen(p)
m = 655656

c1, c2 = encrypt(m, g, h, p)
m1 = decrypt(c1, c2, x, p)

print("original:", m)
print("encrypted:", c1, c2)
print("decrypted:", m1)