#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hệ Chữ Ký Điện Tử RSA
RSA Digital Signature System

Giới thiệu: Ứng dụng thực hiện chữ ký điện tử RSA với giao diện đồ họa
Introduction: Application implementing RSA digital signature with GUI
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow


def main():
    """Hàm chính của ứng dụng - Main application function"""

    # Tạo ứng dụng Qt - Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Hệ Chữ Ký Điện Tử RSA")
    app.setApplicationName("RSA Digital Signature System")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Cryptography Lab")

    # Thiết lập icon cho ứng dụng - Set application icon
    if os.path.exists("icon.png"):
        app.setWindowIcon(QIcon("icon.png"))

    # Thiết lập ngôn ngữ tiếng Việt - Set Vietnamese language
    translator = QTranslator()
    if translator.load(":/translations/vi_VN"):
        app.installTranslator(translator)

    # Tạo và hiển thị cửa sổ chính - Create and show main window
    window = MainWindow()
    window.show()

    # Thiết lập cửa sổ ở trung tâm màn hình - Center window on screen
    window.center_on_screen()

    # Chạy ứng dụng - Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()