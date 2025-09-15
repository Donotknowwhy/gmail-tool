# 🔧 Hướng dẫn khắc phục lỗi Gmail Tool

## ❌ Lỗi 400: Bad Request

### **Nguyên nhân:**
- OAuth consent screen chưa được cấu hình đúng
- Credentials không hợp lệ
- Gmail API chưa được bật

### **Giải pháp:**

#### **Bước 1: Cấu hình OAuth Consent Screen**
1. Vào https://console.cloud.google.com/
2. Chọn project → **APIs & Services** → **OAuth consent screen**
3. **Kiểm tra:**
   - App status: **"In production"** hoặc **"Testing"**
   - Nếu "Testing": Thêm email của bạn vào **"Test users"**
4. Nhấn **"Publish app"** nếu cần

#### **Bước 2: Kiểm tra Gmail API**
1. **APIs & Services** → **Library**
2. Tìm **"Gmail API"** → Nhấn **"Enable"**
3. Đợi vài phút để API được kích hoạt

#### **Bước 3: Tạo lại Credentials**
1. **APIs & Services** → **Credentials**
2. **Delete** OAuth client hiện tại
3. **Create Credentials** → **OAuth client ID**
4. Chọn **"Desktop application"**
5. Tải file JSON mới và đặt tên `credentials.json`

#### **Bước 4: Kiểm tra Redirect URIs**
- Đảm bảo có **"http://localhost"** trong Authorized redirect URIs
- Nếu không có, thêm vào thủ công

---

## ❌ Lỗi: "credentials.json not found"

### **Giải pháp:**
1. Tạo file `credentials.json` từ Google Cloud Console
2. Đặt file vào thư mục chứa `gmail_tool.py`
3. Đảm bảo tên file chính xác (không có số thứ tự)

---

## ❌ Lỗi: "python is not recognized"

### **Giải pháp:**
1. Cài Python từ https://www.python.org/downloads/
2. **Quan trọng:** Tick vào "Add Python to PATH"
3. Restart Command Prompt

---

## ❌ Lỗi: "git is not recognized"

### **Giải pháp:**
1. Cài Git từ https://git-scm.com/download/win
2. Restart Command Prompt

---

## ❌ Lỗi: "Permission denied"

### **Giải pháp:**
1. Chạy Command Prompt với quyền Administrator
2. Hoặc thay đổi quyền thư mục

---

## 💡 Mẹo hay

- **Luôn kiểm tra** OAuth consent screen trước khi tạo credentials
- **Đợi vài phút** sau khi enable API
- **Sử dụng email chính** để test
- **Kiểm tra spam folder** nếu không nhận được email xác thực

---

## 📞 Hỗ trợ

Nếu vẫn gặp vấn đề:
1. Kiểm tra kết nối Internet
2. Thử tạo project mới trong Google Cloud Console
3. Đảm bảo tài khoản Google có quyền truy cập Gmail
