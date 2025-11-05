#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA Cryptographic Engine
Động cơ mật mã RSA

Module này chứa các hàm thực hiện thuật toán RSA
This module contains RSA algorithm implementations
"""

import random
import math
import sympy
from typing import Tuple, Optional, List
import hashlib


class RSAEngine:
    """Lớp thực hiện các thao tác RSA - Class for RSA operations"""

    def __init__(self):
        """Khởi tạo động cơ RSA - Initialize RSA engine"""
        self.p = None  # Số nguyên tố lớn đầu tiên
        self.q = None  # Số nguyên tố lớn thứ hai
        self.n = None  # Module RSA (n = p * q)
        self.phi = None  # Hàm Euler φ(n) = (p-1)(q-1)
        self.e = None  # Số mũ công khai
        self.d = None  # Số mũ bí mật
        self.public_key = None  # Khóa công khai (e, n)
        self.private_key = None  # Khóa bí mật (d, n)

    def is_prime(self, n: int, k: int = 5) -> bool:
        """
        Kiểm tra số nguyên tố bằng Miller-Rabin
        Primality test using Miller-Rabin

        Args:
            n: Số cần kiểm tra - Number to test
            k: Số vòng lặp - Number of iterations

        Returns:
            bool: True nếu là số nguyên tố - True if prime
        """
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False

        # Viết n-1 dưới dạng 2^r * d - Write n-1 as 2^r * d
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1

        # Thực hiện k vòng kiểm tra - Perform k test rounds
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for __ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(self, bit_length: int = 8) -> int:
        """
        Tạo số nguyên tố ngẫu nhiên - Generate random prime number

        Args:
            bit_length: Độ dài bit - Bit length

        Returns:
            int: Số nguyên tố - Prime number
        """
        while True:
            # Tạo số ngẫu nhiên có độ dài bit_length - Generate random number
            num = random.getrandbits(bit_length)
            # Đảm bảo số lẻ và đủ lớn - Ensure odd and large enough
            num |= (1 << bit_length - 1) | 1
            if self.is_prime(num):
                return num

    def generate_keys(self, p: Optional[int] = None, q: Optional[int] = None,
                     e: int = 65537) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Tạo cặp khóa RSA - Generate RSA key pair

        Args:
            p: Số nguyên tố thứ nhất - First prime (optional)
            q: Số nguyên tố thứ hai - Second prime (optional)
            e: Số mũ công khai - Public exponent (default: 65537)

        Returns:
            Tuple[Tuple[int, int], Tuple[int, int]]: ((e, n), (d, n))
        """
        # Tạo hoặc sử dụng số nguyên tố p - Generate or use prime p
        if p is None:
            self.p = self.generate_prime(8)  # 8-bit cho demo - 8-bit for demo
        else:
            if not self.is_prime(p):
                raise ValueError(f"{p} không phải là số nguyên tố - is not prime")
            self.p = p

        # Tạo hoặc sử dụng số nguyên tố q - Generate or use prime q
        if q is None:
            self.q = self.generate_prime(8)
        else:
            if not self.is_prime(q):
                raise ValueError(f"{q} không phải là số nguyên tố - is not prime")
            self.q = q

        # Tính các tham số RSA - Calculate RSA parameters
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = e

        # Tính số mũ bí mật d - Calculate private exponent d
        # e * d ≡ 1 (mod φ(n)) - Modular inverse
        self.d = self.mod_inverse(self.e, self.phi)

        # Tạo cặp khóa - Create key pairs
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

        return self.public_key, self.private_key

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Thuật toán Euclid mở rộng - Extended Euclidean Algorithm
        Tìm x, y sao cho ax + by = gcd(a, b)
        Find x, y such that ax + by = gcd(a, b)

        Args:
            a, b: Số nguyên - Integers

        Returns:
            Tuple[int, int, int]: (gcd, x, y)
        """
        if a == 0:
            return b, 0, 1
        else:
            gcd, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

    def mod_inverse(self, a: int, m: int) -> int:
        """
        Tính nghịch đảo modulo - Compute modular inverse
        Tìm x sao cho a * x ≡ 1 (mod m)
        Find x such that a * x ≡ 1 (mod m)

        Args:
            a: Số cần tìm nghịch đảo - Number to find inverse
            m: Module - Modulus

        Returns:
            int: Nghịch đảo modulo - Modular inverse
        """
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"{a} không có nghịch đảo modulo {m} - has no modular inverse")
        else:
            return x % m

    def hash_message(self, message: str) -> int:
        """
        Băm thông điệp bằng SHA-256 - Hash message with SHA-256

        Args:
            message: Thông điệp cần băm - Message to hash

        Returns:
            int: Giá trị băm dưới dạng số nguyên - Hash value as integer
        """
        hash_obj = hashlib.sha256(message.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        return int(hash_hex, 16)

    def sign(self, message: str, private_key: Optional[Tuple[int, int]] = None) -> int:
        """
        Ký thông điệp - Sign message

        Args:
            message: Thông điệp cần ký - Message to sign
            private_key: Khóa bí mật (d, n) - Private key

        Returns:
            int: Chữ ký số - Digital signature
        """
        if private_key is None:
            private_key = self.private_key

        d, n = private_key

        # Băm thông điệp - Hash message
        hashed_msg = self.hash_message(message)

        # Ký: s = hash(m)^d mod n - Sign: s = hash(m)^d mod n
        signature = pow(hashed_msg, d, n)

        return signature

    def verify(self, message: str, signature: int,
               public_key: Optional[Tuple[int, int]] = None) -> bool:
        """
        Xác thực chữ ký - Verify signature

        Args:
            message: Thông điệp gốc - Original message
            signature: Chữ ký cần xác thực - Signature to verify
            public_key: Khóa công khai (e, n) - Public key

        Returns:
            bool: True nếu chữ ký hợp lệ - True if signature is valid
        """
        if public_key is None:
            public_key = self.public_key

        e, n = public_key

        # Băm thông điệp gốc - Hash original message
        hashed_msg = self.hash_message(message)

        # Xác thực: hash(m) ≡ s^e mod n - Verify: hash(m) ≡ s^e mod n
        decrypted_signature = pow(signature, e, n)

        return (hashed_msg % n) == decrypted_signature

    def get_key_info(self) -> dict:
        """
        Lấy thông tin về các khóa - Get key information

        Returns:
            dict: Thông tin chi tiết về khóa - Detailed key information
        """
        return {
            'p': self.p,
            'q': self.q,
            'n': self.n,
            'phi': self.phi,
            'e': self.e,
            'd': self.d,
            'public_key': self.public_key,
            'private_key': self.private_key
        }

    def rsa_encrypt(self, plaintext: int, public_key: Optional[Tuple[int, int]] = None) -> int:
        """
        Mã hóa RSA - RSA encryption

        Args:
            plaintext: Bản rõ dưới dạng số - Plaintext as number
            public_key: Khóa công khai - Public key

        Returns:
            int: Bản mã - Ciphertext
        """
        if public_key is None:
            public_key = self.public_key

        e, n = public_key
        return pow(plaintext, e, n)

    def rsa_decrypt(self, ciphertext: int, private_key: Optional[Tuple[int, int]] = None) -> int:
        """
        Giải mã RSA - RSA decryption

        Args:
            ciphertext: Bản mã - Ciphertext
            private_key: Khóa bí mật - Private key

        Returns:
            int: Bản rõ - Plaintext
        """
        if private_key is None:
            private_key = self.private_key

        d, n = private_key
        return pow(ciphertext, d, n)


def test_rsa_engine():
    """Hàm kiểm tra động cơ RSA - Test RSA engine"""
    engine = RSAEngine()

    # Tạo khóa - Generate keys
    pub_key, priv_key = engine.generate_keys()
    print(f"Public key: {pub_key}")
    print(f"Private key: {priv_key}")

    # Thông điệp thử nghiệm - Test message
    message = "Hello RSA!"
    print(f"Original message: {message}")

    # Ký thông điệp - Sign message
    signature = engine.sign(message)
    print(f"Signature: {signature}")

    # Xác thực chữ ký - Verify signature
    is_valid = engine.verify(message, signature)
    print(f"Signature valid: {is_valid}")

    # Kiểm tra với thông điệp khác - Test with different message
    fake_message = "Fake message"
    is_fake_valid = engine.verify(fake_message, signature)
    print(f"Fake message signature valid: {is_fake_valid}")


if __name__ == "__main__":
    test_rsa_engine()