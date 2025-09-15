@echo off
echo ========================================
echo    GMAIL TOOL - WINDOWS LAUNCHER
echo ========================================
echo.

REM Kiểm tra Python có được cài đặt không
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt!
    echo Vui lòng tải Python từ: https://www.python.org/downloads/
    echo Nhớ tick vào "Add Python to PATH" khi cài đặt
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt
echo.

REM Kiểm tra virtual environment
if not exist "venv" (
    echo 🔧 Đang tạo virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Không thể tạo virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment đã được tạo
)

REM Kích hoạt virtual environment
echo 🔧 Đang kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Kiểm tra dependencies
if not exist "venv\Lib\site-packages\google" (
    echo 🔧 Đang cài đặt dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Không thể cài đặt dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies đã được cài đặt
)

REM Kiểm tra credentials.json
if not exist "credentials.json" (
    echo ❌ Không tìm thấy file credentials.json
    echo Vui lòng:
    echo 1. Vào https://console.cloud.google.com/
    echo 2. Tạo project và bật Gmail API
    echo 3. Tạo OAuth credentials
    echo 4. Tải file JSON và đặt tên là credentials.json
    echo 5. Đặt file vào thư mục này
    pause
    exit /b 1
)

echo ✅ File credentials.json đã có
echo.

REM Chạy ứng dụng
echo 🚀 Đang khởi động Gmail Tool...
echo.
python gmail_tool.py

REM Tạm dừng để xem kết quả
echo.
echo Nhấn phím bất kỳ để thoát...
pause >nul
