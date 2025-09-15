# 🪟 Hướng dẫn cài đặt Gmail Tool trên Windows

## 📥 Tải và cài đặt Python

### Bước 1: Tải Python
1. Vào trang web: **https://www.python.org/downloads/**
2. Nhấn nút **"Download Python 3.x.x"** (màu vàng lớn)
3. Chờ tải xong file `.exe`

### Bước 2: Cài đặt Python
1. **Mở file vừa tải** (thường ở Downloads)
2. **Quan trọng:** Tick vào ☑️ **"Add Python to PATH"** 
3. Nhấn **"Install Now"**
4. Chờ cài đặt xong → Nhấn **"Close"**

### Bước 3: Kiểm tra Python
1. Nhấn **Windows + R**
2. Gõ `cmd` → Nhấn Enter
3. Gõ: `python --version`
4. Nếu hiện số phiên bản → ✅ Thành công!

---

## 📥 Cài đặt Git

### Bước 1: Tải Git
1. Vào: **https://git-scm.com/download/win**
2. Nhấn **"Download for Windows"** (màu xanh lớn)
3. Chờ tải xong file `.exe`

### Bước 2: Cài đặt Git
1. **Mở file vừa tải** (thường ở Downloads)
2. Nhấn **"Next"** → **"Next"** → **"Next"** → **"Install"**
3. Chờ cài đặt xong → Nhấn **"Finish"**

### Bước 3: Kiểm tra Git
1. Nhấn **Windows + R**
2. Gõ `cmd` → Nhấn Enter
3. Gõ: `git --version`
4. Nếu hiện số phiên bản → ✅ Thành công!

---

## 📁 Clone và thiết lập Gmail Tool

### Bước 1: Clone dự án
1. **Mở Command Prompt**
2. **Clone dự án:**
   ```cmd
   cd C:\
   git clone https://github.com/Donotknowwhy/gmail-tool.git
   cd gmail-tool
   ```

### Bước 2: Cài đặt thư viện
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Chạy ứng dụng

### Lần đầu chạy:
```cmd
cd C:\gmail-tool
venv\Scripts\activate
python gmail_tool.py
```

### Lần sau chạy:
```cmd
cd C:\gmail-tool
venv\Scripts\activate
python gmail_tool.py
```

---

## ✅ Kiểm tra cài đặt

### Cấu trúc thư mục đúng:
```
C:\gmail-tool\
├── gmail_tool.py          ✅
├── credentials.json       ✅ (bạn tự tạo)
├── requirements.txt       ✅
├── run_gmail_tool.bat     ✅
├── WINDOWS_SETUP.md       ✅
├── venv\                 ✅ (tự tạo)
└── token.json            ✅ (tự tạo khi chạy)
```

### Lần đầu chạy thành công:
1. ✅ Tool mở trình duyệt
2. ✅ Chọn tài khoản Gmail
3. ✅ Cấp quyền truy cập
4. ✅ Hiện menu chính

---

## 🔧 Xử lý lỗi

### ❌ "python is not recognized"
**Nguyên nhân:** Chưa tick "Add Python to PATH"
**Giải pháp:** Cài lại Python và tick ☑️ "Add Python to PATH"

### ❌ "git is not recognized"
**Nguyên nhân:** Git chưa được cài đặt
**Giải pháp:** Cài Git từ https://git-scm.com/download/win

### ❌ "credentials.json not found"
**Nguyên nhân:** Thiếu file credentials
**Giải pháp:** Tải file JSON từ Google Cloud và đặt tên `credentials.json`


### ❌ "Permission denied"
**Nguyên nhân:** Không đủ quyền
**Giải pháp:** 
1. Nhấn **Windows + R**
2. Gõ `cmd` → Nhấn **Ctrl + Shift + Enter**
3. Chọn **"Yes"** khi hỏi quyền Administrator

---

## 💡 Mẹo hay

- **Lưu Command Prompt:** Tạo shortcut để mở nhanh
- **Backup token:** Copy file `token.json` để không cần đăng nhập lại
- **Đổi tài khoản:** Chọn option 4 trong menu để đổi Gmail
- **Ngày nhập:** Dùng định dạng DD/MM/YYYY (15/01/2024)

---

**🎉 Chúc bạn cài đặt thành công!**