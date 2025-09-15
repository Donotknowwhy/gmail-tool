# 🪟 Hướng dẫn cài đặt Gmail Tool trên Windows

## 📋 Yêu cầu
- Windows 10/11
- Kết nối Internet
- Tài khoản Gmail

## 🚀 Cài đặt nhanh (5 phút)

### Bước 1: Cài đặt Python
1. Tải Python từ: https://www.python.org/downloads/
2. **Quan trọng:** Tick vào "Add Python to PATH" khi cài đặt
3. Chọn "Install Now"

### Bước 2: Tải dự án
1. Tải ZIP của dự án
2. Giải nén vào thư mục `C:\tool-gmail`

### Bước 3: Chạy ứng dụng
**Cách 1: Sử dụng file batch (Dễ nhất)**
1. Double-click vào file `run_gmail_tool.bat`
2. File sẽ tự động cài đặt và chạy ứng dụng

**Cách 2: Sử dụng Command Prompt**
1. Mở Command Prompt
2. Gõ các lệnh sau:
```cmd
cd C:\tool-gmail
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python gmail_tool.py
```

### Bước 4: Thiết lập Google Cloud
1. Vào: https://console.cloud.google.com/
2. Tạo project mới
3. Bật Gmail API
4. Tạo OAuth 2.0 credentials (Desktop application)
5. Tải file JSON và đặt tên là `credentials.json`
6. Đặt file vào thư mục `C:\tool-gmail`

## 🎯 Sử dụng
1. Chạy ứng dụng
2. Lần đầu sẽ mở trình duyệt để đăng nhập Gmail
3. Cấp quyền cho ứng dụng
4. Sử dụng menu để phân tích email

## 🐛 Xử lý lỗi

### "python is not recognized"
- Cài đặt lại Python và tick "Add Python to PATH"
- Restart Command Prompt

### "credentials.json not found"
- Kiểm tra file có đúng tên và vị trí không
- Đảm bảo đã tải từ Google Cloud Console

### "Permission denied"
- Chạy Command Prompt với quyền Administrator
- Hoặc chạy file `run_gmail_tool.bat` bằng cách right-click → "Run as administrator"

### Lỗi kết nối
- Kiểm tra Internet
- Tắt firewall tạm thời
- Thử lại sau vài phút

## 📁 Cấu trúc thư mục sau khi cài đặt
```
C:\tool-gmail\
├── gmail_tool.py
├── credentials.json      ← Bạn tự tạo
├── run_gmail_tool.bat   ← File chạy nhanh
├── requirements.txt
├── venv\                ← Virtual environment
└── ... (các file khác)
```

## ✅ Kiểm tra cài đặt thành công
Nếu thấy menu như này là thành công:
```
🎯 GMAIL TOOL - CHẾ ĐỘ TƯƠNG TÁC
============================================================

Chọn chức năng:
1. Phân tích đơn hàng theo khoảng thời gian
2. Tìm kiếm email theo từ khóa
3. Xuất kết quả ra file
0. Thoát
```

## 📞 Hỗ trợ
Nếu gặp vấn đề, hãy:
1. Kiểm tra lại các bước trên
2. Xem file README.md chi tiết
3. Liên hệ hỗ trợ
