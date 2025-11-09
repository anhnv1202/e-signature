# QUY TRÌNH HỆ THỐNG CHỮ KÝ ĐIỆN TỬ RSA

## 📋 Tổng Quan

Ứng dụng giáo dục thực hiện hệ chữ ký điện tử RSA với giao diện PyQt6, bao gồm 3 chức năng chính:
- **Tạo khóa RSA**: Sinh cặp khóa công khai và bí mật
- **Ký thông điệp**: Tạo chữ ký số cho văn bản
- **Xác thực chữ ký**: Kiểm tra tính hợp lệ của chữ ký

---

## 🔄 Quy Trình Hoạt Động

### 1. TẠO KHÓA RSA

**Luồng xử lý:**
```
Người dùng nhập p, q, e (hoặc để trống)
    ↓
UI gọi RSAThread (xử lý nền)
    ↓
RSAEngine.generate_keys()
    ├─ Kiểm tra/sinh số nguyên tố p, q
    ├─ Tính n = p × q
    ├─ Tính φ(n) = (p-1)(q-1)
    ├─ Tính d = e⁻¹ mod φ(n) (dùng Extended Euclidean)
    └─ Tạo khóa công khai (e,n) và khóa bí mật (d,n)
    ↓
Hiển thị kết quả lên UI
```

**Ví dụ:**
- p = 61, q = 53
- n = 3233
- φ(n) = 3120
- e = 17
- d = 2753
- **Khóa công khai**: (17, 3233)
- **Khóa bí mật**: (2753, 3233)

---

### 2. KÝ THÔNG ĐIỆP

**Luồng xử lý:**
```
Người dùng nhập thông điệp M
    ↓
RSAEngine.sign()
    ├─ Băm thông điệp: H = SHA-256(M)
    └─ Ký: S = H^d mod n
    ↓
Trả chữ ký S về UI
```

**Công thức:**
- `H = SHA-256(message)`
- `S = H^d mod n`

**Ví dụ:**
- Thông điệp: "HELLO"
- Hash mod n = 820
- Chữ ký: `820^2753 mod 3233 = 1627`

---

### 3. XÁC THỰC CHỮ KÝ

**Luồng xử lý:**
```
Người dùng nhập thông điệp M và chữ ký S
    ↓
RSAEngine.verify()
    ├─ Băm lại thông điệp: H1 = SHA-256(M)
    ├─ Giải mã chữ ký: H2 = S^e mod n
    └─ So sánh: H1 mod n == H2?
    ↓
Trả kết quả (True/False)
```

**Công thức:**
- `H1 = SHA-256(message)`
- `H2 = S^e mod n`
- **Kết luận**: Nếu `H1 mod n == H2` → Chữ ký hợp lệ

**Ví dụ:**
- Thông điệp: "HELLO", Chữ ký: 1627
- H1 mod n = 820
- H2 = `1627^17 mod 3233 = 820`
- `820 == 820` → ✅ **Chữ ký hợp lệ**

---

## 🏗️ Kiến Trúc Code

```
main.py (Entry Point)
    ↓
ui/main_window.py (Giao diện)
    ├─ Tab 1: Tạo Khóa
    ├─ Tab 2: Ký & Xác Thực
    └─ Tab 3: Giải Thích
    ↓
RSAThread (QThread - xử lý nền)
    ↓
crypto/rsa_engine.py (Logic xử lý)
    ├─ generate_keys()
    ├─ sign()
    └─ verify()
    ↓
visualization/math_visualizer.py (Trực quan hóa)
```

---

## 🔧 Các Hàm Toán Học Chính

### Extended Euclidean Algorithm
- Tìm gcd(a, b) và x, y sao cho: `ax + by = gcd(a, b)`
- Dùng để tính nghịch đảo modulo

### Modular Inverse
- Tìm d sao cho: `e × d ≡ 1 (mod φ(n))`
- Sử dụng Extended Euclidean Algorithm

### Miller-Rabin Primality Test
- Kiểm tra số có phải số nguyên tố không

---

## 📊 Tính Năng Bổ Sung

- **Trực quan hóa**: Sơ đồ luồng tạo khóa, ký, xác thực
- **Xử lý nền**: Dùng QThread tránh đơ UI
- **Giao diện tiếng Việt**: Hỗ trợ song ngữ Việt-Anh
- **Hiển thị chi tiết**: Các bước tính toán được hiển thị đầy đủ

---

## ⚠️ Lưu Ý

- **Ứng dụng giáo dục**: Chỉ dùng cho mục đích học tập
- **Kích thước khóa nhỏ**: 8-bit cho demo, không đủ an toàn thực tế
- **Không lưu trữ khóa**: Khóa chỉ tồn tại trong bộ nhớ

---

**Tóm tắt**: Hệ thống thực hiện đầy đủ quy trình chữ ký điện tử RSA từ tạo khóa → ký → xác thực, với giao diện trực quan và trực quan hóa các bước tính toán.


