#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA Digital Signature System Installation Script
Script cài đặt Hệ thống Chữ ký RSA

This script handles the installation of dependencies with fallback options
for compatibility issues.
"""

import sys
import subprocess
import platform


def install_package(package_name, import_name=None):
    """Install a single package with error handling"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"✓ {package_name} is already installed")
        return True
    except ImportError:
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package_name}")
            return False


def install_pyqt6():
    """Install PyQt6 with fallback options"""
    try:
        import PyQt6
        print("✓ PyQt6 is already installed")
        return True
    except ImportError:
        print("Installing PyQt6...")
        try:
            # Try standard installation first
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
            print("✓ PyQt6 installed successfully")
            return True
        except subprocess.CalledProcessError:
            try:
                # Try alternative installation
                subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6", "--no-deps"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6-Qt6"])
                print("✓ PyQt6 installed successfully (alternative method)")
                return True
            except subprocess.CalledProcessError:
                print("✗ Failed to install PyQt6")
                return False


def install_matplotlib():
    """Install matplotlib with fallback options"""
    try:
        import matplotlib
        print("✓ matplotlib is already installed")
        return True
    except ImportError:
        print("Installing matplotlib...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
            print("✓ matplotlib installed successfully")
            return True
        except subprocess.CalledProcessError:
            try:
                # Try without build dependencies
                subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "--only-binary=:all:"])
                print("✓ matplotlib installed successfully (binary version)")
                return True
            except subprocess.CalledProcessError:
                print("✗ Failed to install matplotlib")
                return False


def main():
    """Main installation function"""
    print("="*50)
    print("RSA DIGITAL SIGNATURE SYSTEM INSTALLATION")
    print("CAI DAT HE THONG CHU KY RSA")
    print("="*50)
    print()

    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        return False

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()}")
    print()

    # Install packages
    packages = [
        ("cryptography", "cryptography"),
        ("numpy", "numpy"),
        ("sympy", "sympy"),
    ]

    success_count = 0
    total_packages = len(packages) + 2  # +2 for PyQt6 and matplotlib

    # Install PyQt6
    if install_pyqt6():
        success_count += 1

    # Install matplotlib
    if install_matplotlib():
        success_count += 1

    # Install other packages
    for package_name, import_name in packages:
        if install_package(package_name, import_name):
            success_count += 1

    print()
    print("="*50)
    print(f"Installation completed: {success_count}/{total_packages} packages installed")

    if success_count == total_packages:
        print("✓ All dependencies installed successfully!")
        print()
        print("You can now run the application:")
        print("- Windows: Double-click start.bat")
        print("- Any OS: python run.py")
        print("- Direct: python main.py")
        return True
    else:
        print("✗ Some packages failed to install.")
        print()
        print("Try running these commands manually:")
        print("pip install PyQt6 matplotlib numpy sympy cryptography")
        print()
        print("Or use the simple requirements:")
        print("pip install PyQt6>=6.6.0 matplotlib>=3.7.0 numpy>=1.24.0 sympy>=1.11 cryptography>=41.0.0")
        return False


if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)