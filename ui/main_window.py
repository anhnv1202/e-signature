#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cửa Sổ Chính Giao Diện RSA
Main RSA GUI Window

Module này chứa giao diện đồ họa chính cho hệ chữ ký RSA
This module contains the main GUI for the RSA signature system
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QTabWidget, QScrollArea, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from crypto.rsa_engine import RSAEngine
from visualization.math_visualizer import MathVisualizer


class RSAThread(QThread):
    """Luồng xử lý RSA để tránh treo giao diện - RSA processing thread to avoid UI freezing"""

    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, operation: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs

    def run(self):
        """Thực thi thao tác RSA - Execute RSA operation"""
        try:
            engine = RSAEngine()
            result = {}

            if self.operation == "generate_keys":
                p = self.kwargs.get('p')
                q = self.kwargs.get('q')
                e = self.kwargs.get('e', 65537)

                pub_key, priv_key = engine.generate_keys(p, q, e)
                result = {
                    'success': True,
                    'key_info': engine.get_key_info(),
                    'public_key': pub_key,
                    'private_key': priv_key
                }

            elif self.operation == "sign":
                message = self.kwargs.get('message')
                d = self.kwargs.get('d')
                n = self.kwargs.get('n')

                # Cần gán khóa bí mật đầy đủ để phương thức sign không lấy None
                engine.d = d
                engine.n = n
                engine.private_key = (d, n)
                signature = engine.sign(message)

                result = {
                    'success': True,
                    'signature': signature,
                    'hashed_message': engine.hash_message(message)
                }

            elif self.operation == "verify":
                message = self.kwargs.get('message')
                signature = self.kwargs.get('signature')
                e = self.kwargs.get('e')
                n = self.kwargs.get('n')

                # Tương tự, gán khóa công khai để verify không bị None
                engine.e = e
                engine.n = n
                engine.public_key = (e, n)
                is_valid = engine.verify(message, signature)

                result = {
                    'success': True,
                    'is_valid': is_valid,
                    'hashed_message': engine.hash_message(message),
                    'decrypted_signature': pow(signature, e, n)
                }

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng RSA - Main window of RSA application"""

    def __init__(self):
        super().__init__()
        self.rsa_engine = RSAEngine()
        self.visualizer = MathVisualizer()
        self.current_key_info = {}
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện người dùng - Initialize user interface"""

        # Cài đặt cửa sổ - Window setup
        self.setWindowTitle("Hệ Chữ Ký Điện Tử RSA - RSA Digital Signature System")
        self.setGeometry(100, 100, 1200, 800)

        # Font chữ - Font
        font = QFont("Segoe UI", 10)
        self.setFont(font)

        # Widget trung tâm - Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout chính - Main layout
        main_layout = QVBoxLayout(central_widget)

        # Tiêu đề - Title
        title_label = QLabel("🔐 HỆ THỐNG CHỮ KÝ ĐIỆN TỬ RSA")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("QLabel { color: #2c3e50; margin: 10px; }")
        main_layout.addWidget(title_label)

        # Tạo tab widget - Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Tab 1: Tạo khóa - Key Generation Tab
        self.create_key_generation_tab()

        # Tab 2: Ký và Xác thực - Sign and Verify Tab
        self.create_signature_tab()

        # Tab 3: Giải thích các bước - Step Explanation Tab
        self.create_explanation_tab()

        # Đã bỏ Tab Giới thiệu - About Tab removed per request

        # Thanh trạng thái - Status bar
        self.statusBar().showMessage("Sẵn sàng - Ready")

    def create_key_generation_tab(self):
        """Tạo tab tạo khóa - Create key generation tab"""

        # Widget và layout - Widget and layout
        key_widget = QWidget()
        layout = QVBoxLayout(key_widget)

        # Nhóm tham số đầu vào - Input parameters group
        input_group = QGroupBox("📝 Tham số đầu vào - Input Parameters")
        input_layout = QGridLayout(input_group)

        # Số nguyên tố p - Prime p
        input_layout.addWidget(QLabel("Số nguyên tố p:"), 0, 0)
        self.p_input = QLineEdit()
        self.p_input.setPlaceholderText("Để trống để tạo ngẫu nhiên - Leave empty for random")
        input_layout.addWidget(self.p_input, 0, 1)

        # Số nguyên tố q - Prime q
        input_layout.addWidget(QLabel("Số nguyên tố q:"), 1, 0)
        self.q_input = QLineEdit()
        self.q_input.setPlaceholderText("Để trống để tạo ngẫu nhiên - Leave empty for random")
        input_layout.addWidget(self.q_input, 1, 1)

        # Số mũ công khai e - Public exponent e
        input_layout.addWidget(QLabel("Số mũ công khai e:"), 2, 0)
        self.e_input = QLineEdit("65537")
        input_layout.addWidget(self.e_input, 2, 1)

        # Nút tạo khóa - Generate keys button
        self.generate_btn = QPushButton("🔑 Tạo khóa RSA - Generate RSA Keys")
        self.generate_btn.clicked.connect(self.generate_keys)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        input_layout.addWidget(self.generate_btn, 3, 0, 1, 2)

        # Nút trực quan hóa - Visualization button
        self.visualize_key_btn = QPushButton("📊 Xem Sơ Đồ Tạo Khóa - View Key Generation Diagram")
        self.visualize_key_btn.clicked.connect(self.show_key_generation_diagram)
        self.visualize_key_btn.setEnabled(False)
        self.visualize_key_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #2c3e50;
            }
        """)
        input_layout.addWidget(self.visualize_key_btn, 4, 0, 1, 2)

        layout.addWidget(input_group)

        # Progress bar - Thanh tiến trình
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Nhóm kết quả - Results group
        results_group = QGroupBox("📊 Kết quả - Results")
        results_layout = QGridLayout(results_group)

        # Thông tin khóa - Key information
        self.key_info_text = QTextEdit()
        self.key_info_text.setMaximumHeight(200)
        self.key_info_text.setReadOnly(True)
        results_layout.addWidget(self.key_info_text, 0, 0, 1, 2)

        # Khóa công khai - Public key
        results_layout.addWidget(QLabel("🔓 Khóa công khai (e, n):"), 1, 0)
        self.public_key_label = QLabel("Chưa tạo - Not generated")
        self.public_key_label.setStyleSheet(
            "QLabel { font-family: monospace; background-color: #1e272e; color: #ecf0f1; padding: 8px 10px; border: 1px solid #2c3e50; border-radius: 6px; }"
        )
        results_layout.addWidget(self.public_key_label, 1, 1)

        # Khóa bí mật - Private key
        results_layout.addWidget(QLabel("🔒 Khóa bí mật (d, n):"), 2, 0)
        self.private_key_label = QLabel("Chưa tạo - Not generated")
        self.private_key_label.setStyleSheet(
            "QLabel { font-family: monospace; background-color: #1e272e; color: #ecf0f1; padding: 8px 10px; border: 1px solid #2c3e50; border-radius: 6px; }"
        )
        results_layout.addWidget(self.private_key_label, 2, 1)

        layout.addWidget(results_group)

        # Scroll area - Khu vực cuộn
        scroll = QScrollArea()
        scroll.setWidget(key_widget)
        scroll.setWidgetResizable(True)

        self.tab_widget.addTab(scroll, "🔑 Tạo Khóa - Key Generation")

    def create_signature_tab(self):
        """Tạo tab ký và xác thực - Create sign and verify tab"""

        # Widget và layout - Widget and layout
        sig_widget = QWidget()
        layout = QVBoxLayout(sig_widget)

        # Nhóm ký - Signing group
        sign_group = QGroupBox("✍️ Ký Thông Điệp - Sign Message")
        sign_layout = QVBoxLayout(sign_group)

        # Nhập thông điệp - Message input
        sign_layout.addWidget(QLabel("Thông điệp cần ký - Message to sign:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(80)
        self.message_input.setPlaceholderText("Nhập thông điệp của bạn ở đây - Enter your message here")
        sign_layout.addWidget(self.message_input)

        # Nút ký - Sign button
        self.sign_btn = QPushButton("✍️ Ký thông điệp - Sign Message")
        self.sign_btn.clicked.connect(self.sign_message)
        self.sign_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        sign_layout.addWidget(self.sign_btn)

        # Nút xem sơ đồ ký - View signing diagram button
        self.visualize_sign_btn = QPushButton("📊 Xem Sơ Đồ Ký - View Signing Diagram")
        self.visualize_sign_btn.clicked.connect(self.show_signing_diagram)
        self.visualize_sign_btn.setEnabled(False)
        self.visualize_sign_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #2c3e50;
            }
        """)
        sign_layout.addWidget(self.visualize_sign_btn)

        # Kết quả ký - Signature result
        sign_layout.addWidget(QLabel("Chữ ký số - Digital Signature:"))
        self.signature_result = QTextEdit()
        self.signature_result.setMaximumHeight(60)
        self.signature_result.setReadOnly(True)
        self.signature_result.setStyleSheet(
            "QTextEdit { font-family: monospace; background-color: #1e272e; color: #ecf0f1; border: 1px solid #2c3e50; border-radius: 6px; }"
        )
        sign_layout.addWidget(self.signature_result)

        layout.addWidget(sign_group)

        # Nhóm xác thực - Verification group
        verify_group = QGroupBox("✔️ Xác Thực Chữ Ký - Verify Signature")
        verify_layout = QVBoxLayout(verify_group)

        # Nhập chữ ký - Signature input
        verify_layout.addWidget(QLabel("Chữ ký cần xác thực - Signature to verify:"))
        self.signature_input = QLineEdit()
        self.signature_input.setPlaceholderText("Nhập chữ ký số - Enter digital signature")
        verify_layout.addWidget(self.signature_input)

        # Nút xác thực - Verify button
        self.verify_btn = QPushButton("✔️ Xác thực chữ ký - Verify Signature")
        self.verify_btn.clicked.connect(self.verify_signature)
        self.verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        verify_layout.addWidget(self.verify_btn)

        # Nút xem sơ đồ xác thực - View verification diagram button
        self.visualize_verify_btn = QPushButton("📊 Xem Sơ Đồ Xác Thực - View Verification Diagram")
        self.visualize_verify_btn.clicked.connect(self.show_verification_diagram)
        self.visualize_verify_btn.setEnabled(False)
        self.visualize_verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #2c3e50;
            }
        """)
        verify_layout.addWidget(self.visualize_verify_btn)

        # Kết quả xác thực - Verification result
        self.verify_result = QLabel("Chưa xác thực - Not verified")
        self.verify_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verify_result.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)
        verify_layout.addWidget(self.verify_result)

        layout.addWidget(verify_group)

        # Chi tiết xác thực - Verification details
        details_group = QGroupBox("🔍 Chi Tiết Xác Thực - Verification Details")
        details_layout = QVBoxLayout(details_group)

        self.verify_details = QTextEdit()
        self.verify_details.setReadOnly(True)
        self.verify_details.setMaximumHeight(150)
        self.verify_details.setStyleSheet(
            "QTextEdit { font-family: monospace; background-color: #1e272e; color: #ecf0f1; border: 1px solid #2c3e50; border-radius: 6px; }"
        )
        details_layout.addWidget(self.verify_details)

        layout.addWidget(details_group)

        # Scroll area - Khu vực cuộn
        scroll = QScrollArea()
        scroll.setWidget(sig_widget)
        scroll.setWidgetResizable(True)

        self.tab_widget.addTab(scroll, "✍️ Ký & Xác Thực - Sign & Verify")

    def create_explanation_tab(self):
        """Tạo tab giải thích các bước - Create step explanation tab"""

        explanation_widget = QWidget()
        layout = QVBoxLayout(explanation_widget)

        # Tiêu đề - Title
        title = QLabel("📚 Giải Thích Các Bước Thực Hiện RSA")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Nội dung giải thích - Explanation content
        explanation_text = QTextEdit()
        explanation_text.setReadOnly(True)
        explanation_html = """
        <h2>🔐 Thuật Toán RSA</h2>

        <h3>1. Tạo Khóa - Key Generation</h3>
        <p><strong>Chọn hai số nguyên tố lớn p và q</strong><br>
        - p và q là các số nguyên tố lớn và bí mật<br>
        - Ví dụ: p = 61, q = 53</p>

        <p><strong>Tính n = p × q</strong><br>
        - n là module RSA, được công khai<br>
        - Ví dụ: n = 61 × 53 = 3233</p>

        <p><strong>Tính φ(n) = (p-1) × (q-1)</strong><br>
        - φ(n) là hàm Euler của n<br>
        - Ví dụ: φ(3233) = 60 × 52 = 3120</p>

        <p><strong>Chọn e sao cho 1 < e < φ(n) và gcd(e, φ(n)) = 1</strong><br>
        - e là số mũ công khai<br>
        - Ví dụ: e = 17</p>

        <p><strong>Tính d = e⁻¹ mod φ(n)</strong><br>
        - d là số mũ bí mật<br>
        - Ví dụ: d = 2753</p>

        <h3>2. Ký Thông Điệp - Message Signing</h3>
        <p><strong>Băm thông điệp</strong><br>
        - Sử dụng hàm băm SHA-256<br>
        - H = Hash(message)</p>

        <p><strong>Ký chữ ký</strong><br>
        - S = Hᵈ mod n<br>
        - S là chữ ký số</p>

        <h3>3. Xác Thực Chữ Ký - Signature Verification</h3>
        <p><strong>Tính lại băm</strong><br>
        - H' = Hash(message)</p>

        <p><strong>Giải mã chữ ký</strong><br>
        - S' = Sᵉ mod n</p>

        <p><strong>So sánh</strong><br>
        - Nếu H' = S' thì chữ ký hợp lệ<br>
        - Ngược lại, chữ ký không hợp lệ</p>

        <h3>📝 Tính Toán Mở Rộng - Extended Calculation</h3>
        <p><strong>Thuật toán Euclid mở rộng</strong><br>
        - Tìm x, y sao cho ax + by = gcd(a, b)<br>
        - Dùng để tính nghịch đảo modulo</p>

        <p><strong>Nghịch đảo modulo</strong><br>
        - Tìm x sao cho a × x ≡ 1 (mod m)<br>
        - x là nghịch đảo của a modulo m</p>

        <h3>🔍 Ví Dụ Cụ Thể - Concrete Example</h3>
        <p><strong>Tạo khóa:</strong><br>
        - p = 61, q = 53<br>
        - n = 3233<br>
        - φ(n) = 3120<br>
        - e = 17<br>
        - d = 2753</p>

        <p><strong>Ký thông điệp "HELLO":</strong><br>
        - Hash("HELLO") = 12345678<br>
        - Signature = 12345678²⁷⁵³ mod 3233 = 9876</p>

        <p><strong>Xác thực:</strong><br>
        - 9876¹⁷ mod 3233 = 12345678<br>
        - Hash("HELLO") = 12345678<br>
        - → Chữ ký hợp lệ!</p>
        """

        explanation_text.setHtml(explanation_html)
        layout.addWidget(explanation_text)

        # Nút xem chứng minh toán học - View mathematical proof button
        self.proof_btn = QPushButton("🧮 Xem Chứng Minh Toán Học RSA - View RSA Mathematical Proof")
        self.proof_btn.clicked.connect(self.show_mathematical_proof)
        self.proof_btn.setEnabled(False)
        self.proof_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        layout.addWidget(self.proof_btn)

        self.tab_widget.addTab(explanation_widget, "📚 Giải Thích - Explanation")

    # Removed About tab implementation

    def generate_keys(self):
        """Tạo cặp khóa RSA - Generate RSA key pair"""

        try:
            # Lấy tham số đầu vào - Get input parameters
            p_text = self.p_input.text().strip()
            q_text = self.q_input.text().strip()
            e_text = self.e_input.text().strip()

            p = int(p_text) if p_text else None
            q = int(q_text) if q_text else None
            e = int(e_text) if e_text else 65537

            # Hiển thị progress bar - Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.generate_btn.setEnabled(False)

            # Tạo luồng xử lý - Create processing thread
            self.rsa_thread = RSAThread("generate_keys", p=p, q=q, e=e)
            self.rsa_thread.finished.connect(self.on_keys_generated)
            self.rsa_thread.error.connect(self.on_key_generation_error)
            self.rsa_thread.start()

            self.statusBar().showMessage("Đang tạo khóa... - Generating keys...")

        except ValueError as e:
            QMessageBox.warning(self, "Lỗi đầu vào - Input Error",
                              f"Vui lòng nhập số nguyên hợp lệ - Please enter valid integers:\n{str(e)}")

    def on_keys_generated(self, result):
        """Xử lý kết quả tạo khóa - Handle key generation result"""

        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)

        if result['success']:
            # Lưu thông tin khóa - Save key information
            self.current_key_info = result['key_info']

            # Hiển thị thông tin chi tiết - Show detailed information
            key_info_text = f"""
✅ THÔNG TIN KHÓA RSA - RSA KEY INFORMATION
{'='*50}

🔢 Số nguyên tố - Prime Numbers:
  p = {self.current_key_info['p']}
  q = {self.current_key_info['q']}

🧮 Module RSA - RSA Module:
  n = p × q = {self.current_key_info['n']}

📐 Hàm Euler - Euler's Function:
  φ(n) = (p-1) × (q-1) = {self.current_key_info['phi']}

🔑 Khóa công khai - Public Key:
  e = {self.current_key_info['e']}
  (e, n) = ({self.current_key_info['public_key'][0]}, {self.current_key_info['public_key'][1]})

🔒 Khóa bí mật - Private Key:
  d = {self.current_key_info['d']}
  (d, n) = ({self.current_key_info['private_key'][0]}, {self.current_key_info['private_key'][1]})

✅ Kiểm tra - Verification:
  e × d mod φ(n) = {self.current_key_info['e']} × {self.current_key_info['d']} mod {self.current_key_info['phi']} = {(self.current_key_info['e'] * self.current_key_info['d']) % self.current_key_info['phi']}
"""

            self.key_info_text.setText(key_info_text)
            self.public_key_label.setText(f"({self.current_key_info['public_key'][0]}, {self.current_key_info['public_key'][1]})")
            self.private_key_label.setText(f"({self.current_key_info['private_key'][0]}, {self.current_key_info['private_key'][1]})")

            self.statusBar().showMessage("✅ Tạo khóa thành công! - Key generation successful!")

            # Bật các nút trực quan hóa - Enable visualization buttons
            self.visualize_key_btn.setEnabled(True)
            self.proof_btn.setEnabled(True)

            # Chuyển sang tab ký - Switch to sign tab
            self.tab_widget.setCurrentIndex(1)

        else:
            QMessageBox.error(self, "Lỗi - Error", "Tạo khóa thất bại - Key generation failed")

    def on_key_generation_error(self, error_message):
        """Xử lý lỗi tạo khóa - Handle key generation error"""

        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)

        QMessageBox.critical(self, "Lỗi Tạo Khóa - Key Generation Error",
                           f"Lỗi khi tạo khóa RSA - Error generating RSA keys:\n{error_message}")
        self.statusBar().showMessage("❌ Lỗi tạo khóa - Key generation error")

    def sign_message(self):
        """Ký thông điệp - Sign message"""

        try:
            # Kiểm tra đã tạo khóa chưa - Check if keys exist
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa RSA trước khi ký - Please generate RSA keys before signing")
                return

            # Lấy thông điệp - Get message
            message = self.message_input.toPlainText().strip()
            if not message:
                QMessageBox.warning(self, "Thông điệp rỗng - Empty Message",
                                  "Vui lòng nhập thông điệp cần ký - Please enter message to sign")
                return

            # Vô hiệu hóa nút - Disable button
            self.sign_btn.setEnabled(False)

            # Tạo luồng xử lý - Create processing thread
            d = self.current_key_info['d']
            n = self.current_key_info['n']

            self.sign_thread = RSAThread("sign", message=message, d=d, n=n)
            self.sign_thread.finished.connect(self.on_message_signed)
            self.sign_thread.error.connect(self.on_sign_error)
            self.sign_thread.start()

            self.statusBar().showMessage("Đang ký thông điệp... - Signing message...")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi ký - Signing Error",
                               f"Lỗi khi ký thông điệp - Error signing message:\n{str(e)}")

    def on_message_signed(self, result):
        """Xử lý kết quả ký - Handle signing result"""

        self.sign_btn.setEnabled(True)

        if result['success']:
            # Hiển thị chữ ký - Show signature
            signature_str = str(result['signature'])
            self.signature_result.setText(signature_str)

            # Tự động điền vào ô xác thực - Auto-fill verification field
            self.signature_input.setText(signature_str)

            # Hiển thị thông tin chi tiết - Show detailed information
            details = f"""
✅ THÔNG TIN KÝ - SIGNING INFORMATION
{'='*40}

📝 Thông điệp gốc - Original Message:
  "{self.message_input.toPlainText()}"

🔐 Giá trị băm SHA-256 - SHA-256 Hash Value:
  {result['hashed_message']}

🔒 Dùng khóa bí mật - Using Private Key:
  d = {self.current_key_info['d']}
  n = {self.current_key_info['n']}

✍️ Chữ ký số - Digital Signature:
  S = Hash(M)ᵈ mod n
  S = {result['hashed_message']}^{self.current_key_info['d']} mod {self.current_key_info['n']}
  S = {result['signature']}
"""

            self.verify_details.setText(details)

            # Bật nút trực quan hóa ký - Enable signing visualization button
            self.visualize_sign_btn.setEnabled(True)

            self.statusBar().showMessage("✅ Ký thành công! - Signing successful!")

        else:
            QMessageBox.error(self, "Lỗi ký - Signing Error", "Ký thông điệp thất bại - Signing failed")

    def on_sign_error(self, error_message):
        """Xử lý lỗi ký - Handle signing error"""

        self.sign_btn.setEnabled(True)
        QMessageBox.critical(self, "Lỗi Ký - Signing Error",
                           f"Lỗi khi ký thông điệp - Error signing message:\n{error_message}")
        self.statusBar().showMessage("❌ Lỗi ký - Signing error")

    def verify_signature(self):
        """Xác thực chữ ký - Verify signature"""

        try:
            # Kiểm tra đã tạo khóa chưa - Check if keys exist
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa RSA trước khi xác thực - Please generate RSA keys before verifying")
                return

            # Lấy thông tin - Get information
            message = self.message_input.toPlainText().strip()
            signature_text = self.signature_input.text().strip()

            if not message:
                QMessageBox.warning(self, "Thiếu thông điệp - Missing Message",
                                  "Vui lòng nhập thông điệp gốc - Please enter original message")
                return

            if not signature_text:
                QMessageBox.warning(self, "Thiếu chữ ký - Missing Signature",
                                  "Vui lòng nhập chữ ký cần xác thực - Please enter signature to verify")
                return

            signature = int(signature_text)

            # Vô hiệu hóa nút - Disable button
            self.verify_btn.setEnabled(False)

            # Tạo luồng xử lý - Create processing thread
            e = self.current_key_info['e']
            n = self.current_key_info['n']

            self.verify_thread = RSAThread("verify", message=message,
                                         signature=signature, e=e, n=n)
            self.verify_thread.finished.connect(self.on_signature_verified)
            self.verify_thread.error.connect(self.on_verify_error)
            self.verify_thread.start()

            self.statusBar().showMessage("Đang xác thực... - Verifying...")

        except ValueError:
            QMessageBox.warning(self, "Lỗi định dạng - Format Error",
                              "Chữ ký phải là số nguyên - Signature must be an integer")

    def on_signature_verified(self, result):
        """Xử lý kết quả xác thực - Handle verification result"""

        self.verify_btn.setEnabled(True)

        if result['success']:
            # Hiển thị kết quả - Show result
            is_valid = result['is_valid']

            if is_valid:
                result_text = "✅ CHỮ KÝ HỢP LỆ! - SIGNATURE VALID!"
                result_style = """
                    QLabel {
                        color: white;
                        background-color: #27ae60;
                        font-size: 16px;
                    }
                """
                status_text = "✅ Xác thực thành công! - Verification successful!"
            else:
                result_text = "❌ CHỮ KÝ KHÔNG HỢP LỆ! - SIGNATURE INVALID!"
                result_style = """
                    QLabel {
                        color: white;
                        background-color: #e74c3c;
                        font-size: 16px;
                    }
                """
                status_text = "❌ Xác thực thất bại! - Verification failed!"

            self.verify_result.setText(result_text)
            self.verify_result.setStyleSheet(result_style)

            # Hiển thị chi tiết - Show details
            details = f"""
🔍 THÔNG TIN XÁC THỰC - VERIFICATION INFORMATION
{'='*50}

📝 Thông điệp gốc - Original Message:
  "{self.message_input.toPlainText()}"

🔐 Băm thông điệp - Message Hash:
  Hash(M) = {result['hashed_message']}

🔓 Dùng khóa công khai - Using Public Key:
  e = {self.current_key_info['e']}
  n = {self.current_key_info['n']}

🔍 Giải mã chữ ký - Decrypt Signature:
  Sᵉ mod n = {self.signature_input.text()}^{self.current_key_info['e']} mod {self.current_key_info['n']}
  Sᵉ mod n = {result['decrypted_signature']}

⚖️ So sánh - Comparison:
  Hash(M) = {result['hashed_message']}
  Sᵉ mod n = {result['decrypted_signature']}

  Kết quả - Result: {'Bằng nhau - Equal ✓' if is_valid else 'Khác nhau - Different ✗'}

🎯 Kết luận - Conclusion:
  Chữ ký {'HỢP LỆ - VALID' if is_valid else 'KHÔNG HỢP LỆ - INVALID'}
"""

            self.verify_details.setText(details)

            # Bật nút trực quan hóa xác thực - Enable verification visualization button
            self.visualize_verify_btn.setEnabled(True)

            self.statusBar().showMessage(status_text)

        else:
            QMessageBox.error(self, "Lỗi xác thực - Verification Error", "Xác thực thất bại - Verification failed")

    def on_verify_error(self, error_message):
        """Xử lý lỗi xác thực - Handle verification error"""

        self.verify_btn.setEnabled(True)
        QMessageBox.critical(self, "Lỗi Xác Thực - Verification Error",
                           f"Lỗi khi xác thực chữ ký - Error verifying signature:\n{error_message}")
        self.statusBar().showMessage("❌ Lỗi xác thực - Verification error")

    def show_key_generation_diagram(self):
        """Hiển thị sơ đồ tạo khóa - Show key generation diagram"""
        try:
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa trước khi xem sơ đồ - Please generate keys before viewing diagram")
                return

            # Tạo sơ đồ - Create diagram
            diagram_file = self.visualizer.create_key_generation_flowchart(self.current_key_info)

            # Hiển thị trong cửa sổ mới - Show in new window
            self.show_image_dialog("Sơ Đồ Tạo Khóa RSA - RSA Key Generation Diagram", diagram_file)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi trực quan hóa - Visualization Error",
                               f"Lỗi khi tạo sơ đồ - Error creating diagram:\n{str(e)}")

    def show_signing_diagram(self):
        """Hiển thị sơ đồ quá trình ký - Show signing process diagram"""
        try:
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa trước khi xem sơ đồ - Please generate keys before viewing diagram")
                return

            message = self.message_input.toPlainText().strip()
            if not message:
                QMessageBox.warning(self, "Thiếu thông điệp - Missing Message",
                                  "Vui lòng nhập thông điệp trước khi xem sơ đồ - Please enter message before viewing diagram")
                return

            signature_text = self.signature_result.toPlainText().strip()
            if not signature_text:
                QMessageBox.warning(self, "Chưa ký - Not Signed",
                                  "Vui lòng ký thông điệp trước khi xem sơ đồ - Please sign message before viewing diagram")
                return

            # Tạo sơ đồ - Create diagram
            hashed_msg = self.rsa_engine.hash_message(message)
            signature = int(signature_text)

            diagram_file = self.visualizer.create_signing_process_diagram(
                message, signature, hashed_msg, self.current_key_info
            )

            # Hiển thị trong cửa sổ mới - Show in new window
            self.show_image_dialog("Sơ Đồ Quá Trình Ký - RSA Signing Process Diagram", diagram_file)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi trực quan hóa - Visualization Error",
                               f"Lỗi khi tạo sơ đồ - Error creating diagram:\n{str(e)}")

    def show_verification_diagram(self):
        """Hiển thị sơ đồ quá trình xác thực - Show verification process diagram"""
        try:
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa trước khi xem sơ đồ - Please generate keys before viewing diagram")
                return

            message = self.message_input.toPlainText().strip()
            signature_text = self.signature_input.text().strip()

            if not message or not signature_text:
                QMessageBox.warning(self, "Thiếu thông tin - Missing Information",
                                  "Vui lòng nhập thông điệp và chữ ký trước khi xem sơ đồ - Please enter message and signature before viewing diagram")
                return

            # Lấy thông tin xác thực - Get verification info
            verify_details_text = self.verify_details.toPlainText()
            is_valid = "HỢP LỆ" in verify_details_text

            # Trích xuất thông tin từ chi tiết - Extract info from details
            hashed_msg = self.rsa_engine.hash_message(message)
            signature = int(signature_text)
            e = self.current_key_info['e']
            n = self.current_key_info['n']
            decrypted_signature = pow(signature, e, n)

            verify_info = {
                'hashed_message': hashed_msg,
                'decrypted_signature': decrypted_signature
            }

            # Tạo sơ đồ - Create diagram
            diagram_file = self.visualizer.create_verification_process_diagram(
                message, signature, is_valid, verify_info
            )

            # Hiển thị trong cửa sổ mới - Show in new window
            self.show_image_dialog("Sơ Đồ Quá Trình Xác Thực - RSA Verification Process Diagram", diagram_file)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi trực quan hóa - Visualization Error",
                               f"Lỗi khi tạo sơ đồ - Error creating diagram:\n{str(e)}")

    def show_mathematical_proof(self):
        """Hiển thị chứng minh toán học - Show mathematical proof"""
        try:
            if not self.current_key_info:
                QMessageBox.warning(self, "Chưa có khóa - No Keys",
                                  "Vui lòng tạo khóa trước khi xem chứng minh - Please generate keys before viewing proof")
                return

            # Tạo sơ đồ chứng minh - Create proof diagram
            proof_file = self.visualizer.create_mathematical_proof(self.current_key_info)

            # Hiển thị trong cửa sổ mới - Show in new window
            self.show_image_dialog("Chứng Minh Đúng Đắn RSA - RSA Correctness Proof", proof_file)

        except Exception as e:
            QMessageBox.critical(self, "Lỗi trực quan hóa - Visualization Error",
                               f"Lỗi khi tạo sơ đồ chứng minh - Error creating proof diagram:\n{str(e)}")

    def show_image_dialog(self, title: str, image_path: str):
        """
        Hiển thị hình ảnh trong cửa sổ thoại - Show image in dialog window

        Args:
            title: Tiêu đề cửa sổ - Window title
            image_path: Đường dẫn hình ảnh - Image path
        """
        import PyQt6.QtWidgets as QtW
        import PyQt6.QtGui as QtG

        dialog = QtW.QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(1000, 700)

        layout = QtW.QVBoxLayout(dialog)

        # Hiển thị hình ảnh - Display image
        image_label = QtW.QLabel()
        pixmap = QtG.QPixmap(image_path)
        if not pixmap.isNull():
            # Scale image to fit window
            scaled_pixmap = pixmap.scaled(950, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            image_label.setText("Không thể tải hình ảnh - Cannot load image")

        layout.addWidget(image_label)

        # Buttons - Các nút
        button_layout = QtW.QHBoxLayout()

        save_btn = QtW.QPushButton("💾 Lưu hình ảnh - Save Image")
        save_btn.clicked.connect(lambda: self.save_image(image_path))
        button_layout.addWidget(save_btn)

        close_btn = QtW.QPushButton("Đóng - Close")
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        # Dọn dẹp file tạm khi đóng - Cleanup temp file when closed
        dialog.finished.connect(lambda: self.visualizer.cleanup_temp_file(image_path))

        # Hiển thị cửa sổ - Show dialog
        dialog.exec()

    def save_image(self, image_path: str):
        """
        Lưu hình ảnh - Save image

        Args:
            image_path: Đường dẫn hình ảnh - Image path
        """
        import PyQt6.QtWidgets as QtW

        file_path, _ = QtW.QFileDialog.getSaveFileName(
            self, "Lưu Hình Ảnh - Save Image", "",
            "PNG Files (*.png);;All Files (*)"
        )

        if file_path:
            try:
                import shutil
                shutil.copy2(image_path, file_path)
                QMessageBox.information(self, "Thành công - Success",
                                      f"Hình ảnh đã được lưu tại - Image saved at:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi lưu - Save Error",
                                   f"Không thể lưu hình ảnh - Cannot save image:\n{str(e)}")

    def center_on_screen(self):
        """Căn giữa cửa sổ trên màn hình - Center window on screen"""

        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())