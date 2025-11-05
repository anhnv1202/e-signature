#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical Visualizer for RSA
Trình thị trực quan hóa toán học RSA

Module này cung cấp các công cụ trực quan hóa các bước tính toán RSA
This module provides visualization tools for RSA calculation steps
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from typing import List, Tuple, Dict, Any
import tempfile
import os


class MathVisualizer:
    """Lớp trực quan hóa các bước tính toán RSA - Class for RSA calculation visualization"""

    def __init__(self):
        """Khởi tạo trình thị trực quan - Initialize visualizer"""
        self.figure = Figure(figsize=(12, 8))
        self.canvas = None
        plt.style.use('default')
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#e74c3c',
            'background': '#ecf0f1',
            'text': '#2c3e50',
            'highlight': '#f39c12'
        }

    def create_key_generation_flowchart(self, key_info: Dict[str, Any]) -> str:
        """
        Tạo sơ đồ luồng tạo khóa RSA - Create RSA key generation flowchart

        Args:
            key_info: Thông tin khóa - Key information

        Returns:
            str: Đường dẫn file hình ảnh - Image file path
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')

        # Title - Tiêu đề
        ax.text(5, 11.5, 'Quá Trình Tạo Khóa RSA\nRSA Key Generation Process',
                ha='center', va='center', fontsize=16, fontweight='bold',
                color=self.colors['text'])

        # Flow elements - Các phần tử luồng
        steps = [
            (5, 10, 'Bắt đầu\nStart', 'ellipse', self.colors['primary']),
            (5, 8.5, f'Chọn p = {key_info.get("p", "?")}', 'rectangle', self.colors['background']),
            (5, 7.5, f'Chọn q = {key_info.get("q", "?")}', 'rectangle', self.colors['background']),
            (5, 6.5, f'Tính n = p × q = {key_info.get("n", "?")}', 'rectangle', self.colors['secondary']),
            (5, 5.5, f'Tính φ(n) = (p-1)(q-1) = {key_info.get("phi", "?")}', 'rectangle', self.colors['secondary']),
            (5, 4.5, f'Chọn e = {key_info.get("e", "?")}', 'rectangle', self.colors['background']),
            (5, 3.5, f'Tính d = e⁻¹ mod φ(n) = {key_info.get("d", "?")}', 'rectangle', self.colors['secondary']),
            (5, 2.5, f'Khóa công khai: (e, n) = ({key_info.get("e", "?")}, {key_info.get("n", "?")})', 'rectangle', self.colors['accent']),
            (5, 1.5, f'Khóa bí mật: (d, n) = ({key_info.get("d", "?")}, {key_info.get("n", "?")})', 'rectangle', self.colors['accent']),
            (5, 0.5, 'Hoàn thành\nComplete', 'ellipse', self.colors['primary'])
        ]

        # Draw elements - Vẽ các phần tử
        for x, y, text, shape, color in steps:
            if shape == 'ellipse':
                circle = patches.Ellipse((x, y), 2, 0.8, facecolor=color, edgecolor='black', linewidth=2)
                ax.add_patch(circle)
            else:
                rect = patches.Rectangle((x-1.5, y-0.4), 3, 0.8, facecolor=color, edgecolor='black', linewidth=2)
                ax.add_patch(rect)

            ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

        # Draw arrows - Vẽ mũi tên
        for i in range(len(steps)-1):
            x1, y1, _, _, _ = steps[i]
            x2, y2, _, _, _ = steps[i+1]
            ax.arrow(x1, y1-0.4, 0, y2-y1+0.8, head_width=0.1, head_length=0.1,
                    fc='black', ec='black', linewidth=2)

        # Save image - Lưu hình ảnh
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.tight_layout()
        plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
        plt.close()

        return temp_file.name

    def create_signing_process_diagram(self, message: str, signature: int,
                                     hashed_msg: int, key_info: Dict[str, Any]) -> str:
        """
        Tạo sơ đồ quá trình ký - Create signing process diagram

        Args:
            message: Thông điệp - Message
            signature: Chữ ký - Signature
            hashed_msg: Giá trị băm - Hash value
            key_info: Thông tin khóa - Key information

        Returns:
            str: Đường dẫn file hình ảnh - Image file path
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')

        # Title - Tiêu đề
        ax.text(5, 7.5, 'Quá Trình Ký Thông Điệp RSA\nRSA Message Signing Process',
                ha='center', va='center', fontsize=16, fontweight='bold',
                color=self.colors['text'])

        # Input message - Thông điệp đầu vào
        message_box = patches.Rectangle((0.5, 6), 4, 0.8, facecolor=self.colors['background'],
                                      edgecolor='black', linewidth=2)
        ax.add_patch(message_box)
        ax.text(2.5, 6.4, f'Thông điệp gốc:\n"{message[:50]}{"..." if len(message) > 50 else ""}"',
                ha='center', va='center', fontsize=10)

        # Hash function - Hàm băm
        hash_box = patches.FancyBboxPatch((6, 5.8), 3, 1.2,
                                         boxstyle="round,pad=0.1",
                                         facecolor=self.colors['secondary'],
                                         edgecolor='black', linewidth=2)
        ax.add_patch(hash_box)
        ax.text(7.5, 6.4, 'SHA-256\nHash Function', ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')

        # Arrow from message to hash - Mũi tên từ thông điệp đến hàm băm
        ax.arrow(4.5, 6.4, 1.2, 0, head_width=0.2, head_length=0.1,
                fc='black', ec='black', linewidth=2)

        # Hash value - Giá trị băm
        hash_value_box = patches.Rectangle((0.5, 4.5), 9, 0.8, facecolor=self.colors['highlight'],
                                         edgecolor='black', linewidth=2)
        ax.add_patch(hash_value_box)
        ax.text(5, 4.9, f'H = Hash(M) = {hashed_msg}', ha='center', va='center',
                fontsize=10, fontweight='bold')

        # Arrow from hash to hash value - Mũi tên từ hàm băm xuống giá trị băm
        ax.arrow(7.5, 5.8, 0, -0.5, head_width=0.2, head_length=0.1,
                fc='black', ec='black', linewidth=2)

        # RSA signing - Ký RSA
        sign_box = patches.FancyBboxPatch((6, 2.5), 3, 1.5,
                                         boxstyle="round,pad=0.1",
                                         facecolor=self.colors['accent'],
                                         edgecolor='black', linewidth=2)
        ax.add_patch(sign_box)
        ax.text(7.5, 3.25, 'RSA Signing\nS = Hᵈ mod n', ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')

        # Private key info - Thông tin khóa bí mật
        ax.text(1, 3.5, f'Private Key:\nd = {key_info.get("d", "?")}\nn = {key_info.get("n", "?")}',
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['background']))

        # Arrow from hash value to signing - Mũi tên từ giá trị băm xuống khối ký
        ax.arrow(7.5, 4.5, 0, -0.4, head_width=0.2, head_length=0.1,
                fc='black', ec='black', linewidth=2)

        # Signature result - Kết quả chữ ký
        signature_box = patches.Rectangle((0.5, 0.8), 9, 1, facecolor=self.colors['primary'],
                                        edgecolor='black', linewidth=2)
        ax.add_patch(signature_box)
        ax.text(5, 1.3, f'Chữ ký số - Digital Signature:\nS = {signature}', ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')

        # Arrow from signing to signature - Mũi tên từ khối ký xuống kết quả chữ ký
        ax.arrow(7.5, 2.5, 0, -0.6, head_width=0.2, head_length=0.1,
                fc='black', ec='black', linewidth=2)

        # Save image - Lưu hình ảnh
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.tight_layout()
        plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
        plt.close()

        return temp_file.name

    def create_verification_process_diagram(self, message: str, signature: int,
                                          is_valid: bool, verify_info: Dict[str, Any]) -> str:
        """
        Tạo sơ đồ quá trình xác thực - Create verification process diagram

        Args:
            message: Thông điệp - Message
            signature: Chữ ký - Signature
            is_valid: Kết quả xác thực - Verification result
            verify_info: Thông tin xác thực - Verification information

        Returns:
            str: Đường dẫn file hình ảnh - Image file path
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Title - Tiêu đề
        ax.text(5, 9.5, 'Quá Trình Xác Thực Chữ Ký RSA\nRSA Signature Verification Process',
                ha='center', va='center', fontsize=16, fontweight='bold',
                color=self.colors['text'])

        # Message input - Thông điệp đầu vào
        msg_box = patches.Rectangle((0.5, 8), 4, 0.8, facecolor=self.colors['background'],
                                   edgecolor='black', linewidth=2)
        ax.add_patch(msg_box)
        ax.text(2.5, 8.4, f'Thông điệp:\n"{message[:30]}{"..." if len(message) > 30 else ""}"',
                ha='center', va='center', fontsize=10)

        # Signature input - Chữ ký đầu vào
        sig_box = patches.Rectangle((5.5, 8), 4, 0.8, facecolor=self.colors['background'],
                                   edgecolor='black', linewidth=2)
        ax.add_patch(sig_box)
        ax.text(7.5, 8.4, f'Chữ ký:\n{signature}', ha='center', va='center', fontsize=10)

        # Hash message - Băm thông điệp
        hash1_box = patches.FancyBboxPatch((0.5, 6), 4, 1,
                                          boxstyle="round,pad=0.1",
                                          facecolor=self.colors['secondary'],
                                          edgecolor='black', linewidth=2)
        ax.add_patch(hash1_box)
        ax.text(2.5, 6.5, 'Hash Message\nH1 = Hash(M)', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Decrypt signature - Giải mã chữ ký
        decrypt_box = patches.FancyBboxPatch((5.5, 6), 4, 1,
                                           boxstyle="round,pad=0.1",
                                           facecolor=self.colors['secondary'],
                                           edgecolor='black', linewidth=2)
        ax.add_patch(decrypt_box)
        ax.text(7.5, 6.5, 'Decrypt Signature\nH2 = Sᵉ mod n', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Hash values - Giá trị băm
        hash1_val = patches.Rectangle((0.5, 4.5), 4, 0.8, facecolor=self.colors['highlight'],
                                     edgecolor='black', linewidth=2)
        ax.add_patch(hash1_val)
        ax.text(2.5, 4.9, f'H1 = {verify_info.get("hashed_message", "?")}', ha='center', va='center',
                fontsize=9, fontweight='bold')

        hash2_val = patches.Rectangle((5.5, 4.5), 4, 0.8, facecolor=self.colors['highlight'],
                                     edgecolor='black', linewidth=2)
        ax.add_patch(hash2_val)
        ax.text(7.5, 4.9, f'H2 = {verify_info.get("decrypted_signature", "?")}', ha='center', va='center',
                fontsize=9, fontweight='bold')

        # Comparison - So sánh
        comparison_color = self.colors['secondary'] if is_valid else self.colors['accent']
        comp_box = patches.FancyBboxPatch((3, 2.5), 4, 1.5,
                                         boxstyle="round,pad=0.1",
                                         facecolor=comparison_color,
                                         edgecolor='black', linewidth=2)
        ax.add_patch(comp_box)

        result_text = "✅ EQUAL\nValid Signature" if is_valid else "❌ NOT EQUAL\nInvalid Signature"
        ax.text(5, 3.25, result_text, ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

        # Arrows - Mũi tên
        ax.arrow(2.5, 8.4, 0, -0.9, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)
        ax.arrow(7.5, 8.4, 0, -0.9, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)
        ax.arrow(2.5, 6, 0, -1.0, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)
        ax.arrow(7.5, 6, 0, -1.0, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)
        # Diagonal arrows from H1/H2 bottom-center to the TOP edge center of result box
        ax.arrow(2.5, 4.5, 1.2, -0.5, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)
        ax.arrow(7.5, 4.5, -1.2, -0.5, head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=2)

        # Save image - Lưu hình ảnh
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.tight_layout()
        plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
        plt.close()

        return temp_file.name

    def create_mathematical_proof(self, key_info: Dict[str, Any]) -> str:
        """
        Tạo sơ đồ chứng minh toán học - Create mathematical proof diagram

        Args:
            key_info: Thông tin khóa - Key information

        Returns:
            str: Đường dẫn file hình ảnh - Image file path
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Title - Tiêu đề
        ax.text(5, 9.5, 'Chứng Minh Đúng Đắn RSA\nRSA Correctness Proof',
                ha='center', va='center', fontsize=16, fontweight='bold',
                color=self.colors['text'])

        # Theorem - Định lý
        theorem_box = patches.FancyBboxPatch((0.5, 7.5), 9, 1.2,
                                            boxstyle="round,pad=0.1",
                                            facecolor=self.colors['primary'],
                                            edgecolor='black', linewidth=2)
        ax.add_patch(theorem_box)
        ax.text(5, 8.1, 'Định lý - Theorem:\n(Mᵈ)ᵉ ≡ M (mod n) với M là thông điệp',
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')

        # Proof steps - Các bước chứng minh
        proof_steps = [
            (1, 6.5, 'Cho - Given:'),
            (1, 6, f'p = {key_info.get("p", "?")}, q = {key_info.get("q", "?")}, n = p×q = {key_info.get("n", "?")}'),
            (1, 5.5, f'φ(n) = (p-1)(q-1) = {key_info.get("phi", "?")}'),
            (1, 5, f'e × d ≡ 1 (mod φ(n)) → e × d = k × φ(n) + 1'),
            (1, 4.5, ''),
            (1, 4, 'Chứng minh - Proof:'),
            (1, 3.5, '(Mᵈ)ᵉ = M^{key_info.get("e", "?") × key_info.get("d", "?")}'),
            (1, 3, f'= M^{key_info.get("phi", "?")} × k + 1'),
            (1, 2.5, '= (M^{key_info.get("phi", "?")})ᵏ × M¹'),
            (1, 2, f'= (1 mod p)ᵏ × M (theo định lý nhỏ Fermat)'),
            (1, 1.5, f'= M (mod p) và M (mod q)'),
            (1, 1, '→ M (mod n) theo định lý số dư Trung Hoa'),
            (1, 0.5, '✅ Đpcm - QED')
        ]

        for x, y, text in proof_steps:
            ax.text(x, y, text, fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.2", facecolor=self.colors['background'], alpha=0.8))

        # Highlight important result - Làm nổi bật kết quả quan trọng
        highlight_box = patches.Rectangle((6, 1.5), 3.5, 1, facecolor=self.colors['highlight'],
                                        edgecolor='black', linewidth=2)
        ax.add_patch(highlight_box)
        ax.text(7.75, 2, 'Kết quả - Result:\n(Mᵈ)ᵉ ≡ M (mod n)', ha='center', va='center',
                fontsize=11, fontweight='bold')

        # Save image - Lưu hình ảnh
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.tight_layout()
        plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
        plt.close()

        return temp_file.name

    def create_euclidean_algorithm_visualization(self, a: int, b: int) -> str:
        """
        Tạo trực quan hóa thuật toán Euclid - Create Euclidean algorithm visualization

        Args:
            a, b: Số nguyên - Integers

        Returns:
            str: Đường dẫn file hình ảnh - Image file path
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')

        # Title - Tiêu đề
        ax.text(5, 7.5, f'Thuật Toán Euclid Mở Rộng\nExtended Euclidean Algorithm for {a} and {b}',
                ha='center', va='center', fontsize=14, fontweight='bold',
                color=self.colors['text'])

        # Calculate steps - Tính các bước
        steps = []
        original_a, original_b = a, b

        while b != 0:
            q = a // b
            r = a % b
            steps.append((a, b, q, r))
            a, b = b, r

        # Display steps - Hiển thị các bước
        y_pos = 6
        for i, (a_i, b_i, q_i, r_i) in enumerate(steps):
            # Equation - Phương trình
            equation = f"{a_i} = {b_i} × {q_i} + {r_i}"
            ax.text(1, y_pos, f"Bước {i+1} - Step {i+1}: {equation}", fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['background']))

            # Visual representation - Trực quan hóa
            if r_i > 0:
                # Show division - Hiển thị phép chia
                ax.bar([2], [a_i], width=0.8, color=self.colors['primary'], alpha=0.7)
                ax.bar([3], [b_i * q_i], width=0.8, color=self.colors['secondary'], alpha=0.7)
                ax.bar([4], [r_i], width=0.8, color=self.colors['accent'], alpha=0.7)

                ax.text(2, a_i + 0.2, str(a_i), ha='center', fontsize=9)
                ax.text(3, b_i * q_i + 0.2, f"{b_i}×{q_i}", ha='center', fontsize=9)
                ax.text(4, r_i + 0.2, str(r_i), ha='center', fontsize=9)

                ax.text(2.5, -0.5, "a", ha='center', fontsize=10, fontweight='bold')
                ax.text(3.5, -0.5, "b×q", ha='center', fontsize=10, fontweight='bold')
                ax.text(4.5, -0.5, "r", ha='center', fontsize=10, fontweight='bold')

            y_pos -= 1.2

        # Final result - Kết quả cuối cùng
        gcd = a
        ax.text(1, y_pos, f"gcd({original_a}, {original_b}) = {gcd}", fontsize=12,
               bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['highlight']),
               fontweight='bold')

        # Save image - Lưu hình ảnh
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.tight_layout()
        plt.savefig(temp_file.name, dpi=150, bbox_inches='tight')
        plt.close()

        return temp_file.name

    def cleanup_temp_file(self, file_path: str):
        """
        Xóa file tạm - Clean up temporary file

        Args:
            file_path: Đường dẫn file - File path
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass  # Ignore cleanup errors


def test_visualizer():
    """Hàm kiểm tra trình thị trực quan - Test visualizer"""
    visualizer = MathVisualizer()

    # Test data - Dữ liệu thử nghiệm
    key_info = {
        'p': 61,
        'q': 53,
        'n': 3233,
        'phi': 3120,
        'e': 17,
        'd': 2753
    }

    # Generate visualizations - Tạo trực quan hóa
    flowchart_file = visualizer.create_key_generation_flowchart(key_info)
    signing_file = visualizer.create_signing_process_diagram(
        "Hello RSA", 12345, 67890, key_info
    )
    verification_file = visualizer.create_verification_process_diagram(
        "Hello RSA", 12345, True, {"hashed_message": 67890, "decrypted_signature": 67890}
    )
    proof_file = visualizer.create_mathematical_proof(key_info)
    euclidean_file = visualizer.create_euclidean_algorithm_visualization(3120, 17)

    print("Visualization files created:")
    print(f"- Flowchart: {flowchart_file}")
    print(f"- Signing: {signing_file}")
    print(f"- Verification: {verification_file}")
    print(f"- Proof: {proof_file}")
    print(f"- Euclidean: {euclidean_file}")


if __name__ == "__main__":
    test_visualizer()