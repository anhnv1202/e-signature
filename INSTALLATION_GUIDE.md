# RSA Digital Signature System - Installation Guide
# Hệ Thống Chữ Ký Điện Tử RSA - Hướng Dẫn Cài Đặt

## 🚀 Quick Start (Windows) - Khởi Động Nhanh (Windows)

### Option 1: Easiest Method - Cách dễ nhất
1. Install Python 3.9+ from python.org
2. Open Command Prompt as Administrator
3. Run these commands:
   ```cmd
   pip install PyQt6
   cd e-signature
   python main_simple.py
   ```

### Option 2: Use Installation Script - Dùng Script Cài Đặt
```cmd
python install.py
```

### Option 3: Double-click - Nháy đúp
- Double-click `start.bat` file

## 🔧 Detailed Installation - Cài Đặt Chi Tiết

### Prerequisites - Điều Kiện Tiên Quyết
- **Python 3.9+** (Download from python.org)
- **pip** (Usually comes with Python)
- **4GB RAM minimum** - 4GB RAM tối thiểu

### Installation Methods - Phương Pháp Cài Đặt

#### Method 1: Automatic Installation (Recommended) - Cài Đặt Tự Động (Khuyên dùng)
```bash
python install.py
```
This script will:
- Check Python version
- Install all required dependencies
- Handle common installation errors
- Provide feedback on success/failure

#### Method 2: Manual Installation - Cài Đặt Thủ Công
```bash
# Basic version (minimum requirements)
pip install PyQt6

# Full version with all features
pip install PyQt6 matplotlib numpy sympy cryptography

# Or use the requirements file
pip install -r requirements.txt
```

#### Method 3: Virtual Environment (Recommended for developers) - Môi Trường Ảo
```bash
# Create virtual environment
python -m venv rsa_env

# Activate (Windows)
rsa_env\Scripts\activate

# Activate (Linux/macOS)
source rsa_env/bin/activate

# Install dependencies
pip install PyQt6 matplotlib numpy sympy cryptography

# Run application
python main.py
```

## 🐛 Troubleshooting - Xử Lý Lỗi

### Common Issues - Vấn Đề Phổ Biến

#### 1. "ModuleNotFoundError: No module named 'PyQt6'"
**Solution - Giải pháp:**
```bash
pip install PyQt6
```

#### 2. "Failed building wheel for Pillow/matplotlib"
**Solution - Giải pháp:**
```bash
# Use pre-compiled binaries
pip install --only-binary=:all: matplotlib

# Or use the simple version without matplotlib
python main_simple.py
```

#### 3. "Python version not supported"
**Solution - Giải pháp:**
- Install Python 3.9 or higher from python.org
- Make sure Python is added to PATH

#### 4. "pip command not found"
**Solution - Giải pháp:**
- Reinstall Python and make sure "Add Python to PATH" is checked
- Or use: `python -m pip install <package>`

#### 5. "Permission denied"
**Solution - Giải pháp:**
```bash
# Windows: Run as Administrator
# Linux/macOS: Use sudo
sudo pip install PyQt6

# Or use user directory
pip install --user PyQt6
```

### Alternative Solutions - Giải Pháp Thay Thế

#### If PyQt6 installation fails:
1. **Use the command-line version:**
   ```bash
   python simple_test.py
   ```

2. **Use the web-based version:** (if available)
3. **Use the simple GUI version:**
   ```bash
   python main_simple.py
   ```

## 🎯 Running the Application - Chạy Ứng Dụng

### Method 1: Main Application (Full Features) - Ứng Dụng Chính (Đầy Đủ Tính Năng)
```bash
python main.py
```
**Features:**
- Full GUI interface
- Mathematical visualizations
- All RSA operations
- Vietnamese language support

### Method 2: Simple Application (Basic Features) - Ứng Dụng Đơn Giản (Tính Năng Cơ Bản)
```bash
python main_simple.py
```
**Features:**
- Basic GUI interface
- Core RSA operations
- No matplotlib dependency
- Easier installation

### Method 3: Command Line Only - Chỉ Dòng Lệnh
```bash
python simple_test.py
```
**Features:**
- No GUI required
- Test RSA operations
- Educational output

### Method 4: Interactive Demo - Demo Tương Tác
```bash
python simple_test.py demo
```

## 📋 Verification - Kiểm Tra

### Test if installation was successful - Kiểm tra cài đặt thành công:
```bash
python simple_test.py
```

**Expected output - Kết quả mong đợi:**
```
RSA Digital Signature System Test
========================================
1. Testing key generation...
   Public key (e, n): (65537, 41567)
   Private key (d, n): (17393, 41567)
   [OK] Key generation successful

2. Testing message signing...
   [OK] Message signing successful

3. Testing signature verification...
   [OK] Signature verification successful

4. Testing wrong message verification...
   [OK] Wrong message correctly rejected

5. Testing mathematical properties...
   [OK] Modular inverse property verified

6. Testing hash consistency...
   [OK] Hash function is deterministic

========================================
ALL TESTS PASSED SUCCESSFULLY!
```

## 🔗 System Requirements - Yêu Cầu Hệ Thống

### Minimum Requirements - Tối Thiểu:
- **OS:** Windows 7+, macOS 10.14+, Ubuntu 18.04+
- **Python:** 3.9 or higher
- **RAM:** 4GB
- **Storage:** 100MB free space
- **Processor:** Any modern CPU

### Recommended Requirements - Khuyên Dùng:
- **OS:** Windows 10/11, macOS 12+, Ubuntu 20.04+
- **Python:** 3.11 or higher
- **RAM:** 8GB
- **Storage:** 500MB free space
- **Processor:** Multi-core processor

## 📞 Support - Hỗ Trợ

### Getting Help - Nhận Trợ Giúp:
1. **Check this guide first** - Kiểm tra hướng dẫn này trước
2. **Run the test script** - Chạy script kiểm tra
3. **Check error messages** - Kiểm tra thông báo lỗi
4. **Google the error** - Tìm kiếm lỗi trên Google

### Contact Information - Thông Tin Liên Hệ:
- **Email:** [your-email@example.com]
- **GitHub Issues:** [repository-url]/issues
- **Documentation:** README_VI.md

## 📝 Additional Notes - Ghi Chú Thêm

### Security Warning - Cảnh Báo An Toàn:
- ⚠️ **This is educational software only!**
- ❌ **Do NOT use for real security applications!**
- ✅ **Use for learning and demonstration only!**

### Development Notes - Ghi Chú Phát Triển:
- Source code is fully commented in Vietnamese and English
- All cryptographic operations are implemented from scratch
- Mathematical algorithms are clearly explained
- Code follows Python best practices

---

**Last updated:** December 2025
**Version:** 1.0.0