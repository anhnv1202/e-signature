# Hệ Thống Chữ Ký Điện Tử RSA
# RSA Digital Signature System

## Giới Thiệu - Introduction

Đây là ứng dụng giáo dục thực hiện hệ chữ ký điện tử RSA với giao diện đồ họa bằng Python và PyQt6. Ứng dụng được thiết kế để giúp người dùng hiểu rõ nguyên lý hoạt động của chữ ký số RSA thông qua các bước trực quan hóa chi tiết.

This is an educational application implementing RSA digital signature system with graphical interface using Python and PyQt6. The application is designed to help users understand the working principle of RSA digital signatures through detailed visualizations.

## Tính Năng - Features

### ✅ Hoàn Chỉnh - Completed Features

1. **Tạo Khóa RSA - RSA Key Generation**
   - Tự động tạo số nguyên tố p và q
   - Tính toán module n và hàm Euler φ(n)
   - Tính khóa công khai (e, n) và khóa bí mật (d, n)
   - Hỗ trợ nhập tham số tùy chỉnh

2. **Ký Thông Điệp - Message Signing**
   - Băm thông điệp bằng thuật toán SHA-256
   - Ký thông điệp bằng khóa bí mật RSA
   - Hiển thị chi tiết quá trình tính toán

3. **Xác Thực Chữ Ký - Signature Verification**
   - Xác thực chữ ký bằng khóa công khai RSA
   - So sánh kết quả băm và giải mã chữ ký
   - Hiển thị kết quả hợp lệ/không hợp lệ

4. **Trực Quan Hóa Toán Học - Mathematical Visualization**
   - Sơ đồ luồng tạo khóa RSA
   - Sơ đồ quá trình ký thông điệp
   - Sơ đồ quá trình xác thực chữ ký
   - Chứng minh đúng đắn toán học RSA

5. **Giao Diện Tiếng Việt - Vietnamese Interface**
   - Toàn bộ giao diện bằng tiếng Việt
   - Hỗ trợ song ngữ Việt-Anh
   - Thiết kế trực quan, dễ sử dụng

## Cài Đặt - Installation

### Yêu Cầu Hệ Thống - System Requirements

- Python 3.9 trở lên - Python 3.9 or higher
- Windows/Linux/macOS
- 4GB RAM tối thiểu - 4GB RAM minimum

### Các Bước Cài Đặt - Installation Steps

#### **Phương án 1: Dùng script cài đặt (Khuyên dùng)**
#### **Method 1: Use installation script (Recommended)**

1. **Clone/P Download Repository**
   ```bash
   git clone <repository-url>
   cd e-signature
   ```

2. **Chạy script cài đặt - Run installation script**
   ```bash
   python install.py
   ```

3. **Chạy ứng dụng - Run application**
   ```bash
   python run.py
   ```

#### **Phương án 2: Cài đặt thủ công**
#### **Method 2: Manual installation**

1. **Tạo Môi Trường Ảo - Create Virtual Environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

2. **Cài Đặt Thư Viện - Install Dependencies**
   ```bash
   pip install PyQt6 matplotlib numpy sympy cryptography
   ```

3. **Chạy Ứng Dụng - Run Application**
   ```bash
   python main.py
   ```

#### **Phương án 3: Phiên bản đơn giản (Không cần matplotlib)**
#### **Method 3: Simple version (No matplotlib required)**

1. **Chỉ cài đặt các thư viện cơ bản - Install basic packages only**
   ```bash
   pip install PyQt6
   ```

2. **Chạy phiên bản đơn giản - Run simple version**
   ```bash
   python main_simple.py
   ```

#### **Chạy nhanh**

- Chạy bằng menu tiện lợi: `python run.py`
- Hoặc chạy trực tiếp ứng dụng: `python main.py`

### Build file thực thi (Windows)

Tạo file .exe bằng PyInstaller (đóng gói một file, giao diện cửa sổ, kèm icon):

```bash
python -m PyInstaller --clean --noconfirm --onefile --windowed \
  --icon="icon.png" --add-data "icon.png;." \
  main.py
```

Sau khi hoàn tất, file thực thi nằm tại `dist/`.

## Hướng Dẫn Sử Dụng - User Guide

### 1. Tạo Khóa RSA - RSA Key Generation

**Bước 1 - Step 1:** Mở ứng dụng và chọn tab "Tạo Khóa" - Open application and select "Key Generation" tab

**Bước 2 - Step 2:**
- Để trống để tạo số nguyên tố ngẫu nhiên, hoặc - Leave empty for random primes, or
- Nhập p và q cụ thể - Enter specific p and q values
- Nhập e (mặc định 65537) - Enter e (default 65537)

**Bước 3 - Step 3:** Nhấn nút "Tạo khóa RSA" - Click "Generate RSA Keys" button

**Bước 4 - Step 4:** Xem kết quả khóa công khai và bí mật - View public and private key results

### 2. Ký Thông Điệp - Message Signing

**Bước 1 - Step 1:** Chuyển sang tab "Ký & Xác Thực" - Switch to "Sign & Verify" tab

**Bước 2 - Step 2:** Nhập thông điệp cần ký - Enter message to sign

**Bước 3 - Step 3:** Nhấn nút "Ký thông điệp" - Click "Sign Message" button

**Bước 4 - Step 4:** Sao chép chữ ký kết quả - Copy the resulting signature

### 3. Xác Thực Chữ Ký - Signature Verification

**Bước 1 - Step 1:** Dán thông điệp gốc vào ô thông điệp - Paste original message in message field

**Bước 2 - Step 2:** Dán chữ ký vào ô chữ ký - Paste signature in signature field

**Bước 3 - Step 3:** Nhấn nút "Xác thực chữ ký" - Click "Verify Signature" button

**Bước 4 - Step 4:** Xem kết quả xác thực - View verification result

### 4. Xem Sơ Đồ Trực Quan - View Visualization Diagrams

**Tạo Khóa:** Nhấn "Xem Sơ Đồ Tạo Khóa" sau khi tạo khóa - Click "View Key Generation Diagram" after key generation

**Ký Thông Điệp:** Nhấn "Xem Sơ Đồ Ký" sau khi ký thông điệp - Click "View Signing Diagram" after signing

**Xác Thực:** Nhấn "Xem Sơ Đồ Xác Thực" sau khi xác thực - Click "View Verification Diagram" after verification

**Chứng Minh Toán Học:** Nhấn "Xem Chứng Minh Toán Học" trong tab Giải Thích - Click "View Mathematical Proof" in Explanation tab

## Cấu Trúc Project - Project Structure

```
e-signature/
├── main.py                     # File chính chạy ứng dụng - Main application file
├── requirements.txt            # Danh sách thư viện cần thiết - Required libraries
├── Description.md              # Yêu cầu dự án - Project requirements
├── README_VI.md               # Tài liệu tiếng Việt - Vietnamese documentation
├── docs/                      # Tài liệu - Documentation
│   └── phan_tich_he_thong.md  # Báo cáo phân tích code + ảnh minh họa
├── crypto/                    # Mô-đun mã hóa - Cryptography module
│   ├── __init__.py
│   └── rsa_engine.py          # Động cơ RSA - RSA engine
├── ui/                        # Mô-đun giao diện - UI module
│   ├── __init__.py
│   └── main_window.py         # Cửa sổ chính - Main window
└── visualization/             # Mô-đun trực quan hóa - Visualization module
    ├── __init__.py
    └── math_visualizer.py     # Trình thị trực quan - Visualizer
```

## Giải Thuật Toán RSA - RSA Algorithm

### 1. Tạo Khóa - Key Generation

1. **Chọn hai số nguyên tố lớn p và q** - Choose two large prime numbers p and q
2. **Tính n = p × q** - Compute n = p × q (RSA modulus)
3. **Tính φ(n) = (p-1) × (q-1)** - Compute Euler's totient function
4. **Chọn e sao cho 1 < e < φ(n) và gcd(e, φ(n)) = 1** - Choose public exponent e
5. **Tính d = e⁻¹ mod φ(n)** - Compute private exponent d

### 2. Ký Thông Điệp - Message Signing

1. **Băm thông điệp M** - Hash message M: H = Hash(M)
2. **Ký chữ ký S** - Sign signature S: S = Hᵈ mod n

### 3. Xác Thực Chữ Ký - Signature Verification

1. **Băm thông điệp gốc M** - Hash original message M: H' = Hash(M)
2. **Giải mã chữ ký S** - Decrypt signature S: S' = Sᵉ mod n
3. **So sánh** - Compare: H' ≟ S'

## Ví Dụ Cụ Thể - Concrete Example

### Tham Số - Parameters

```
p = 61, q = 53
n = p × q = 3233
φ(n) = (p-1) × (q-1) = 3120
e = 17
d = 2753
```

### Quá Trình Ký - Signing Process

```
Thông điệp: "HELLO"
Hash("HELLO") = 249687...0661
Hash mod n = 820
Chữ ký = 820²⁷⁵³ mod 3233 = 1627
```

### Quá Trình Xác Thực - Verification Process

```
Chữ ký: 1627
1627¹⁷ mod 3233 = 820
Hash("HELLO") mod 3233 = 820
820 = 820 → Chữ ký hợp lệ!
```

## Kiểm Tra Hệ Thống - System Testing

### Chạy Kiểm Tra - Run Tests

```bash
# Kiểm tra đơn giản - Simple test
python simple_test.py

# Kiểm tra gỡ lỗi - Debug test
python debug_test.py

# Chế độ demo tương tác - Interactive demo
python simple_test.py demo
```

### Kết Quả Kiểm Tra - Test Results

Tất cả các test đều qua thành công:
- ✅ Tạo khóa RSA
- ✅ Ký và xác thực chữ ký
- ✅ Thuộc tính toán học
- ✅ Tính nhất quán hàm băm
- ✅ Từ chối thông điệp sai

## Lưu Ý Quan Trọng - Important Notes

### ⚠️ Cảnh Báo An Toàn - Security Warning

**ĐÂY LÀ ỨNG DỤNG GIÁO DỤC! - THIS IS AN EDUCATIONAL APPLICATION!**

- **KHÔNG** sử dụng cho mục đích thương mại - **DO NOT** use for commercial purposes
- **KHÔNG** sử dụng cho bảo mật thực tế - **DO NOT** use for actual security
- Chỉ dùng cho học tập và giảng dạy - Only for educational and teaching purposes
- Các khóa được tạo với kích thước nhỏ chỉ để demo - Keys are small for demonstration only

### Hạn Chế - Limitations

1. **Kích thước khóa nhỏ** - Small key sizes for demonstration
2. **Không có lưu trữ khóa** - No key storage functionality
3. **Không có quản lý certificate** - No certificate management
4. **Chỉ hỗ trợ văn bản đơn giản** - Only supports simple text

## Kỹ Thuật Phát Triển - Development Technical

### Công Nghệ - Technologies

- **Ngôn ngữ:** Python 3.9+
- **Giao diện:** PyQt6
- **Mật mã:** Tự triển khai + hashlib
- **Trực quan hóa:** Matplotlib
- **Kiểm tra:** Python unittest

### Mẫu Mã - Design Patterns

- **MVC Pattern:** Tách biệt logic và giao diện - Separate logic and UI
- **Multithreading:** Tránh treo giao diện - Prevent UI freezing
- **Error Handling:** Xử lý lỗi toàn diện - Comprehensive error handling

## Hỗ Trợ và Phản Hồi - Support and Feedback

### Liên Hệ - Contact

- Email: [your-email@example.com]
- GitHub: [your-username]
- Documentation: [link-to-docs]

### Báo Cáo Lỗi - Bug Reports

Nếu phát hiện lỗi, vui lòng báo cáo:
- Mô tả chi tiết lỗi - Detailed error description
- Các bước tái hiện - Steps to reproduce
- Hệ thống đang sử dụng - Your system information
- File log nếu có - Log files if available

### Đóng Góp - Contributions

Mọi đóng góp đều được chào đón:
- Report bugs
- Request features
- Submit pull requests
- Improve documentation

## Tài Liệu Tham Khảo - References

1. **Rivest, R., Shamir, A., Adleman, L. (1978)** - "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems"
2. **Menezes, A., van Oorschot, P., Vanstone, S. (1996)** - "Handbook of Applied Cryptography"
3. **Stallings, W. (2017)** - "Cryptography and Network Security: Principles and Practice"

## Lịch Sử Phiên Bản - Version History

### v1.0.0 (2025)
- ✅ Hoàn thiện các tính năng cơ bản - Complete basic features
- ✅ Giao diện tiếng Việt đầy đủ - Full Vietnamese interface
- ✅ Trực quan hóa toán học - Mathematical visualization
- ✅ Hệ thống kiểm tra toàn diện - Comprehensive testing

## Giấy Phép - License

Được phát hành dưới Giấy phép MIT - Released under MIT License

---

**Phát triển cho mục đích giáo dục - Developed for educational purposes**

*Last updated: November 2025*
