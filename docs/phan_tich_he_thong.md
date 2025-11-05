## Phân tích code + hình minh họa hệ chữ ký RSA

Chỉ tập trung vào các bước: Tạo khóa → Ký → Xác thực. Mỗi bước có trích dẫn code và ảnh minh họa (lưu từ ứng dụng).

### 1) Tạo khóa RSA (Key Generation)

Người dùng nhập p, q, e (hoặc để trống để sinh ngẫu nhiên), sau đó bấm “Tạo khóa RSA”. Nút này tạo một luồng nền để tính toán rồi trả kết quả hiển thị lên UI.

Code chính cho tạo khóa (trích):

```103:132:crypto/rsa_engine.py
def generate_keys(self, p: Optional[int] = None, q: Optional[int] = None,
                 e: int = 65537) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # ...
    self.n = self.p * self.q
    self.phi = (self.p - 1) * (self.q - 1)
    self.e = e
    self.d = self.mod_inverse(self.e, self.phi)
    self.public_key = (self.e, self.n)
    self.private_key = (self.d, self.n)
    return self.public_key, self.private_key
```

Luồng gọi từ UI (tạo luồng và nhận kết quả):

```44:56:ui/main_window.py
if self.operation == "generate_keys":
    p = self.kwargs.get('p')
    q = self.kwargs.get('q')
    e = self.kwargs.get('e', 65537)
    pub_key, priv_key = engine.generate_keys(p, q, e)
    result = { 'success': True, 'key_info': engine.get_key_info(),
               'public_key': pub_key, 'private_key': priv_key }
```

Hình minh họa: Sau khi tạo khóa → “📊 Xem Sơ Đồ Tạo Khóa” → “Lưu hình ảnh” → `docs/assets/key_generation.png`.

### 2) Ký thông điệp (Sign)

Quy trình: Băm thông điệp bằng SHA-256 → nâng lũy thừa với số mũ bí mật d modulo n.

Hàm băm và ký:

```173:209:crypto/rsa_engine.py
def hash_message(self, message: str) -> int:
    hash_obj = hashlib.sha256(message.encode('utf-8'))
    return int(hash_obj.hexdigest(), 16)

def sign(self, message: str, private_key: Optional[Tuple[int, int]] = None) -> int:
    if private_key is None:
        private_key = self.private_key
    d, n = private_key
    hashed_msg = self.hash_message(message)
    signature = pow(hashed_msg, d, n)
    return signature
```

Luồng UI (gán khóa và gọi ký trong luồng nền):

```57:70:ui/main_window.py
elif self.operation == "sign":
    message = self.kwargs.get('message')
    d = self.kwargs.get('d'); n = self.kwargs.get('n')
    engine.d = d; engine.n = n; engine.private_key = (d, n)
    signature = engine.sign(message)
    result = { 'success': True, 'signature': signature,
               'hashed_message': engine.hash_message(message) }
```

Hình minh họa: Sau khi ký → “📊 Xem Sơ Đồ Ký” → “Lưu hình ảnh” → `docs/assets/signing.png`.

### 3) Xác thực chữ ký (Verify)

Quy trình: Băm lại thông điệp → giải mã chữ ký với e,n → so sánh hai giá trị.

Thuật toán xác thực:

```211:235:crypto/rsa_engine.py
def verify(self, message: str, signature: int,
           public_key: Optional[Tuple[int, int]] = None) -> bool:
    if public_key is None:
        public_key = self.public_key
    e, n = public_key
    hashed_msg = self.hash_message(message)
    decrypted_signature = pow(signature, e, n)
    return (hashed_msg % n) == decrypted_signature
```

Luồng UI đặt khóa công khai và gọi verify:

```72:87:ui/main_window.py
elif self.operation == "verify":
    message = self.kwargs.get('message')
    signature = self.kwargs.get('signature')
    e = self.kwargs.get('e'); n = self.kwargs.get('n')
    engine.e = e; engine.n = n; engine.public_key = (e, n)
    is_valid = engine.verify(message, signature)
    result = { 'success': True, 'is_valid': is_valid,
               'hashed_message': engine.hash_message(message),
               'decrypted_signature': pow(signature, e, n) }
```

Hình minh họa: Sau khi xác thực → “📊 Xem Sơ Đồ Xác Thực” → “Lưu hình ảnh” → `docs/assets/verification.png`.
### Phụ lục: Hàm hỗ trợ toán học dùng trong bước tạo khóa

```134:171:crypto/rsa_engine.py
def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
    # ... tính gcd và hệ số Bézout

def mod_inverse(self, a: int, m: int) -> int:
    gcd, x, _ = self.extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} không có nghịch đảo modulo {m}")
    return x % m
```

Hết.


