from sympy.ntheory import isprime, primefactors


def find_primitive_root(p):
    if not isprime(p):
        return None

    phi = p - 1
    factors = set(primefactors(phi))

    for g in range(2, p):
        is_primitive = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                is_primitive = False
                break

        if is_primitive:
            return g

    return None


class FileCrypter:
    @staticmethod
    def encrypt(message: bytes, key: int) -> bytes:
        result = bytearray()
        for i, byte in enumerate(message):
            key_part = key >> (i % 32) & 0xFF
            encrypted_byte = byte ^ key_part
            result.append(encrypted_byte)
        return result

    @staticmethod
    def decrypt(message: bytes, key: int) -> bytes:
        result = bytearray()
        for i, byte in enumerate(message):
            key_part = key >> (i % 32) & 0xFF
            encrypted_byte = byte ^ key_part
            result.append(encrypted_byte)
        return result


class DiffieHellman:

    def __init__(self, a: int, p: int):
        self.a = a
        self.p = p
        self.g = find_primitive_root(p)

    @property
    def mixed_key(self):
        return self.g ** self.a % self.p

    def public_key(self):
        return self.g, self.p, self.mixed_key

    def generate_key(self, mixed_key):
        return mixed_key ** self.a % self.p