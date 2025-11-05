@echo off
chcp 65001 >nul
title RSA Digital Signature System - Hệ Thống Chữ Ký Điện Tử RSA

echo ========================================
echo RSA DIGITAL SIGNATURE SYSTEM
echo HE THONG CHU KY DIEN TU RSA
echo ========================================
echo.

echo Starting RSA Digital Signature System...
echo Đang khởi chạy Hệ thống Chữ ký RSA...
echo.

python run.py

if errorlevel 1 (
    echo.
    echo An error occurred. Please check the error message above.
    echo Đã xảy ra lỗi. Vui lòng kiểm tra thông báo lỗi ở trên.
    pause
)