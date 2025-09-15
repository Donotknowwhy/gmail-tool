# Gmail Tool - Công cụ phân tích Email Gmail

Tool đơn giản để phân tích email Gmail, tự động phân loại email đơn hàng thành công/thất bại và trích xuất số đơn hàng.

## ⚡ Cài đặt nhanh (Windows)

1. **Cài Python:** https://www.python.org/downloads/ → Tick "Add Python to PATH"
2. **Tải dự án:** Giải nén vào `C:\gmail-tool`
3. **Chạy:** Double-click `run_gmail_tool.bat`

**📖 Hướng dẫn chi tiết:** Xem file `WINDOWS_SETUP.md`

## 🎯 Tính năng chính

- ✅ **Phân tích email đơn hàng** theo khoảng thời gian
- 🔍 **Tìm kiếm email** theo từ khóa
- 📤 **Xuất kết quả** ra file
- 🔄 **Đổi tài khoản Gmail** dễ dàng

## 📋 Yêu cầu

- **Windows 10/11**
- **Kết nối Internet**
- **Tài khoản Gmail**

## 🚀 Cài đặt nhanh (5 phút)

### Bước 1: Cài Python
1. Vào https://www.python.org/downloads/
2. Tải **Python 3.9+** (nút Download lớn)
3. **Quan trọng:** Tick vào ☑️ **"Add Python to PATH"**
4. Nhấn **Install Now**

### Bước 2: Tải và chạy tool
1. **Tải dự án:** Giải nén ZIP vào thư mục `C:\gmail-tool`
2. **Mở Command Prompt:**
   - Nhấn `Windows + R`
   - Gõ `cmd` và nhấn Enter
3. **Chạy các lệnh:**
   ```cmd
   cd C:\gmail-tool
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Bước 3: Chạy ứng dụng

**Cách 1: Chạy tự động (Khuyến nghị)**
- **Double-click** vào file `run_gmail_tool.bat`
- Tool sẽ tự động kiểm tra và cài đặt mọi thứ

**Cách 2: Chạy thủ công**
```cmd
python gmail_tool.py
```

## 🎮 Cách sử dụng

### Lần đầu chạy:
1. Tool mở trình duyệt → Chọn tài khoản Gmail
2. Cấp quyền truy cập email
3. Tool tự động lưu thông tin đăng nhập

### Menu chính:
```
Chọn chức năng:
1. Phân tích đơn hàng theo khoảng thời gian
2. Tìm kiếm email theo từ khóa  
3. Xuất kết quả ra file
4. Đổi tài khoản Google (xóa token)
0. Thoát
```

### Đổi tài khoản Gmail:
- Chọn **option 4** → Xác nhận xóa token
- Lần sau chạy tool sẽ yêu cầu đăng nhập lại

## 📁 Cấu trúc thư mục

```
C:\gmail-tool\
├── gmail_tool.py          ← File chính
├── credentials.json       ← File bạn tự tạo
├── requirements.txt       ← Danh sách thư viện
├── venv\                 ← Môi trường Python
└── token.json            ← Tự động tạo (có thể xóa)
```

## 🔧 Xử lý lỗi thường gặp

### ❌ "python is not recognized"
**Giải pháp:** Cài lại Python và tick ☑️ "Add Python to PATH"

### ❌ "credentials.json not found"  
**Giải pháp:** Đảm bảo file `credentials.json` có trong thư mục `C:\gmail-tool`

### ❌ "Permission denied"
**Giải pháp:** Chạy Command Prompt với quyền Administrator

## 💡 Mẹo sử dụng

- **Ngày nhập:** Dùng định dạng DD/MM/YYYY (ví dụ: 15/01/2024)
- **Mặc định:** Ngày bắt đầu = 1 tháng trước, Ngày kết thúc = ngày mai
- **Token:** File `token.json` có thể xóa để đăng nhập lại
- **Kết quả:** Tool tự động phân loại email thành COMPLETE/ERROR

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. ✅ Python đã cài đúng
2. ✅ File `credentials.json` có trong thư mục
3. ✅ Kết nối Internet ổn định
4. ✅ Gmail API đã được bật

---

**🎉 Chúc bạn sử dụng tool thành công!**