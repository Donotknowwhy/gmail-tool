# Gmail Tool - Công cụ phân tích Email Gmail

Công cụ phân tích email Gmail với khả năng lọc và phân loại thông minh theo từ khóa trong tiêu đề thư.

Tool này giúp bạn truy cập và phân tích email từ Gmail với các tính năng lọc và phân loại thông minh.

## 🚀 Tính năng chính

- **Truy cập Gmail**: Lấy toàn bộ email từ tài khoản Gmail của bạn
- **Lọc thông minh**: Lọc email theo ngày, tháng, năm, tiêu đề, người gửi
- **Phân tích nội dung**: Tự động phân loại email dựa trên từ khóa:
  - Email chứa "abc" → **COMPLETE**
  - Email chứa "xyz" → **ERROR**
- **Giao diện thân thiện**: Chế độ tương tác dễ sử dụng
- **Xuất kết quả**: Lưu kết quả phân tích ra file

## 📋 Yêu cầu hệ thống

- **Python 3.7+** (khuyến nghị Python 3.9+)
- **Tài khoản Gmail** với quyền truy cập
- **Google Cloud Project** với Gmail API được bật
- **Kết nối Internet** để truy cập Gmail API

## 🛠️ Cài đặt

### **Bước 1: Cài đặt Python**

#### **Windows:**
1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. **Quan trọng:** Tick vào "Add Python to PATH" khi cài đặt
3. Mở Command Prompt và kiểm tra:
```cmd
python --version
```

#### **macOS:**
```bash
# Sử dụng Homebrew
brew install python3

# Hoặc tải từ python.org
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### **Bước 2: Tải và thiết lập dự án**

1. **Tải dự án:**
```bash
# Nếu có Git
git clone <repository-url>
cd tool-gmail

# Hoặc tải ZIP và giải nén
```

2. **Tạo Virtual Environment (Khuyến nghị):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Cài đặt dependencies:**
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux (nếu gặp lỗi externally-managed-environment)
pip3 install -r requirements.txt
```

3. **Thiết lập Google Cloud Console:**
   - Truy cập [Google Cloud Console](https://console.cloud.google.com/)
   - Tạo project mới hoặc chọn project hiện có
   - Bật Gmail API
   - Tạo OAuth 2.0 credentials
   - Tải file JSON credentials và đặt tên là `credentials.json` trong thư mục gốc

## 🎯 Cách sử dụng

### **Chạy tool:**

#### **Windows:**
```cmd
# Kích hoạt virtual environment
venv\Scripts\activate

# Chạy tool
python gmail_tool.py
```

#### **macOS/Linux:**
```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Chạy tool
python3 gmail_tool.py
```

### **Lần đầu chạy:**
1. Tool sẽ mở trình duyệt để đăng nhập Gmail
2. Chọn tài khoản Gmail muốn sử dụng
3. Cấp quyền cho tool truy cập email
4. Tool sẽ tự động lưu token để lần sau không cần đăng nhập lại

### Các chức năng chính:

1. **Lấy email mới nhất**: Lấy danh sách email gần đây nhất
2. **Tìm kiếm email**: Tìm email theo từ khóa trong tiêu đề hoặc nội dung
3. **Lọc theo ngày**: Lọc email trong khoảng thời gian cụ thể
4. **Phân tích email**: Phân tích và đánh dấu trạng thái email
5. **Xuất kết quả**: Lưu kết quả ra file text

### Ví dụ sử dụng trong code:

```python
from gmail_tool import GmailTool

# Khởi tạo tool
tool = GmailTool()
tool.initialize()

# Lấy email mới nhất
emails = tool.fetch_emails(max_results=100)

# Lọc email theo ngày
filtered_emails = tool.filter_emails(
    emails, 
    date_from='2024-01-01',
    date_to='2024-12-31',
    subject_contains='important'
)

# Phân tích nội dung
analyzed_emails = tool.analyze_emails(filtered_emails)

# Hiển thị kết quả
tool.display_emails(analyzed_emails)

# Xuất ra file
tool.export_results(analyzed_emails, 'my_emails.txt')
```

## ⚙️ Cấu hình

Bạn có thể tùy chỉnh các từ khóa phân tích trong file `config.py`:

```python
# Từ khóa để đánh dấu COMPLETE
COMPLETE_KEYWORDS = ['abc', 'done', 'completed']

# Từ khóa để đánh dấu ERROR  
ERROR_KEYWORDS = ['xyz', 'error', 'failed']
```

## 📁 Cấu trúc dự án

```
tool-gmail/
├── gmail_tool.py          # File chính
├── gmail_auth.py          # Xác thực Gmail API
├── email_fetcher.py       # Lấy email từ Gmail
├── email_filter.py        # Lọc email theo tiêu chí
├── content_analyzer.py    # Phân tích nội dung email
├── config.py              # Cấu hình
├── requirements.txt       # Dependencies
├── README.md             # Hướng dẫn sử dụng
├── credentials.json      # File credentials (cần tự tạo)
└── token.json           # File token (tự động tạo)
```

## 🔒 Bảo mật

- File `credentials.json` chứa thông tin nhạy cảm, không commit vào git
- File `token.json` được tạo tự động và có thể xóa để yêu cầu đăng nhập lại
- Tool chỉ có quyền đọc email (readonly), không thể chỉnh sửa

## 🐛 Xử lý lỗi thường gặp

### **Lỗi cài đặt:**

1. **"python is not recognized" (Windows):**
   - Cài đặt Python từ [python.org](https://www.python.org/downloads/)
   - Tick vào "Add Python to PATH" khi cài đặt
   - Restart Command Prompt

2. **"externally-managed-environment" (macOS/Linux):**
   ```bash
   # Sử dụng virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

3. **"pip is not recognized" (Windows):**
   ```cmd
   # Cài đặt pip
   python -m ensurepip --upgrade
   ```

### **Lỗi chạy ứng dụng:**

1. **"credentials.json not found":**
   - Đảm bảo file `credentials.json` có trong thư mục gốc
   - Kiểm tra tên file phải chính xác (không có số thứ tự)

2. **"OAuth consent screen not configured":**
   - Làm lại bước thiết lập OAuth consent screen trong Google Cloud Console
   - Thêm email của bạn vào danh sách Test Users

3. **"API not enabled":**
   - Kiểm tra Gmail API đã được bật trong Google Cloud Console
   - Đợi vài phút để API được kích hoạt

4. **"Quota exceeded":**
   - Gmail API có giới hạn request
   - Giảm số lượng email lấy hoặc đợi reset quota

5. **"Permission denied" (Windows):**
   ```cmd
   # Chạy Command Prompt với quyền Administrator
   # Hoặc thay đổi quyền thư mục
   ```

### **Lỗi kết nối:**

1. **"Connection timeout":**
   - Kiểm tra kết nối Internet
   - Tắt firewall/tường lửa tạm thời
   - Thử lại sau vài phút

2. **"SSL Certificate error":**
   ```bash
   # Cập nhật certificates
   pip install --upgrade certifi
   ```

## 🚀 Hướng dẫn nhanh cho Windows

### **Cài đặt nhanh (5 phút):**

1. **Tải Python:** [python.org](https://www.python.org/downloads/) → Download → Tick "Add Python to PATH"

2. **Tải dự án:** Giải nén ZIP vào thư mục `C:\tool-gmail`

3. **Mở Command Prompt:**
   ```cmd
   cd C:\tool-gmail
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Thiết lập Google Cloud:**
   - Vào [console.cloud.google.com](https://console.cloud.google.com/)
   - Tạo project → Bật Gmail API → Tạo OAuth credentials
   - Tải `credentials.json` vào thư mục `C:\tool-gmail`

5. **Chạy ứng dụng:**
   ```cmd
   python gmail_tool.py
   ```

### **Cấu trúc thư mục sau khi cài đặt:**
```
C:\tool-gmail\
├── gmail_tool.py
├── credentials.json  ← File này bạn tự tạo
├── requirements.txt
├── venv\            ← Virtual environment
└── ... (các file khác)
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub hoặc liên hệ qua email.

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.
