@echo off
title Gmail Tool - Công cụ phân tích Email Gmail
color 0A

echo.
echo ========================================
echo    GMAIL TOOL - CÔNG CỤ PHÂN TÍCH EMAIL
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ LỖI: Python chưa được cài đặt hoặc chưa được thêm vào PATH
    echo.
    echo 📋 HƯỚNG DẪN KHẮC PHỤC:
    echo 1. Tải Python từ: https://www.python.org/downloads/
    echo 2. Cài đặt và TICK vào "Add Python to PATH"
    echo 3. Restart máy tính
    echo 4. Chạy lại file này
    echo.
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt
echo.

REM Kiểm tra thư mục hiện tại
if not exist "gmail_tool.py" (
    echo ❌ LỖI: Không tìm thấy file gmail_tool.py
    echo.
    echo 📋 HƯỚNG DẪN KHẮC PHỤC:
    echo 1. Đảm bảo bạn đang ở trong thư mục chứa Gmail Tool
    echo 2. Kiểm tra file gmail_tool.py có tồn tại không
    echo.
    pause
    exit /b 1
)

echo ✅ Tìm thấy file gmail_tool.py
echo.

REM Kiểm tra virtual environment
if not exist "venv" (
    echo ⚠️  Virtual environment chưa được tạo
    echo 🔧 Đang tạo virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ LỖI: Không thể tạo virtual environment
        pause
        exit /b 1
    )
    echo ✅ Đã tạo virtual environment
)

echo ✅ Virtual environment đã sẵn sàng
echo.

REM Kích hoạt virtual environment
echo 🔧 Đang kích hoạt virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ LỖI: Không thể kích hoạt virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment đã được kích hoạt
echo.

REM Kiểm tra và cài đặt dependencies
if not exist "venv\Lib\site-packages\google" (
    echo ⚠️  Thư viện chưa được cài đặt
    echo 🔧 Đang cài đặt thư viện...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ LỖI: Không thể cài đặt thư viện
        pause
        exit /b 1
    )
    echo ✅ Đã cài đặt thư viện
)

echo ✅ Thư viện đã sẵn sàng
echo.

REM Kiểm tra file credentials
if not exist "credentials.json" (
    echo ⚠️  CẢNH BÁO: Không tìm thấy file credentials.json
    echo.
    echo 📋 HƯỚNG DẪN:
    echo 1. Đảm bảo bạn đã có file credentials.json từ Google Cloud Console
    echo 2. Đặt file vào thư mục này
    echo.
    echo Bạn có muốn tiếp tục không? (y/n)
    set /p choice=
    if /i "%choice%" neq "y" (
        echo 👋 Tạm biệt!
        pause
        exit /b 0
    )
)

echo ✅ File credentials đã sẵn sàng
echo.

REM Chạy ứng dụng
echo 🚀 Đang khởi động Gmail Tool...
echo.
echo ========================================
echo.

python gmail_tool.py

REM Kiểm tra lỗi khi chạy
if errorlevel 1 (
    echo.
    echo ❌ Ứng dụng gặp lỗi khi chạy
    echo.
    echo 📋 CÁC LỖI THƯỜNG GẶP:
    echo 1. credentials.json không đúng định dạng
    echo 2. Kết nối Internet không ổn định
    echo 3. Chưa cấp quyền truy cập Gmail
    echo.
    echo 💡 HƯỚNG DẪN KHẮC PHỤC:
    echo - Kiểm tra file credentials.json
    echo - Kiểm tra kết nối Internet
    echo - Đảm bảo đã cấp quyền truy cập Gmail
    echo.
)

echo.
echo ========================================
echo 👋 Cảm ơn bạn đã sử dụng Gmail Tool!
echo ========================================
echo.
pause