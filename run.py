#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA Digital Signature System Launcher
Trình khởi chạy Hệ thống Chữ ký RSA

This script provides an easy way to run the RSA Digital Signature System
with proper environment setup and error handling.
"""

import sys
import os
import subprocess
import platform


def check_python_version():
    """Kiểm tra phiên bản Python - Check Python version"""
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True


def check_dependencies():
    """Kiểm tra và cài đặt các thư viện cần thiết - Check and install required libraries"""
    try:
        import PyQt6
        print("✓ PyQt6 is installed")
    except ImportError:
        print("✗ PyQt6 is not installed")
        return False

    try:
        import matplotlib
        print("✓ matplotlib is installed")
    except ImportError:
        print("✗ matplotlib is not installed")
        return False

    try:
        import numpy
        print("✓ numpy is installed")
    except ImportError:
        print("✗ numpy is not installed")
        return False

    try:
        import sympy
        print("✓ sympy is installed")
    except ImportError:
        print("✗ sympy is not installed")
        return False

    try:
        from PIL import Image
        print("✓ Pillow is installed")
    except ImportError:
        print("✗ Pillow is not installed")
        return False

    return True


def install_dependencies():
    """Cài đặt các thư viện cần thiết - Install required libraries"""
    print("\nInstalling required libraries...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies!")
        return False


def run_application():
    """Chạy ứng dụng chính - Run main application"""
    try:
        print("\n" + "="*50)
        print("RSA DIGITAL SIGNATURE SYSTEM")
        print("HE THONG CHU KY DIEN TU RSA")
        print("="*50)
        print("\nStarting application...\n")

        # Import and run the main application
        from main import main
        main()

    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please make sure all files are present and dependencies are installed.")
        return False
    except Exception as e:
        print(f"✗ Application error: {e}")
        return False

    return True


def show_menu():
    """Hiển thị menu lựa chọn - Show selection menu"""
    print("\n" + "="*40)
    print("RSA DIGITAL SIGNATURE SYSTEM")
    print("HE THONG CHU KY DIEN TU RSA")
    print("="*40)
    print("\nSelect option - Chọn lựa chọn:")
    print("1. Run Application - Chạy ứng dụng")
    print("2. Install Dependencies - Cài đặt thư viện")
    print("3. Exit - Thoát")
    print()


def main():
    """Hàm chính - Main function"""

    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return

    while True:
        show_menu()
        choice = input("Enter choice (1-3) - Nhập lựa chọn (1-3): ").strip()

        if choice == '1':
            # Check dependencies before running
            if not check_dependencies():
                print("\nDependencies missing. Installing now...")
                if not install_dependencies():
                    input("Press Enter to continue...")
                    continue

            # Run the application
            if not run_application():
                input("\nPress Enter to continue...")

        elif choice == '2':
            # Install dependencies
            if install_dependencies():
                print("\n✓ Dependencies installed successfully!")
            else:
                print("\n✗ Failed to install dependencies!")
            input("Press Enter to continue...")

        elif choice == '3':
            print("\nGoodbye - Tam biet!")
            break

        else:
            print("\n✗ Invalid choice! Please enter 1-3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()