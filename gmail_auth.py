"""
Module xác thực Gmail API
"""
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE


class GmailAuthenticator:
    def __init__(self):
        self.service = None
        self.creds = None
    
    def authenticate(self):
        """Xác thực với Gmail API"""
        # Kiểm tra token đã lưu
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Nếu không có credentials hợp lệ, yêu cầu người dùng đăng nhập
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    print(f"❌ Không tìm thấy file {CREDENTIALS_FILE}")
                    print("\n📋 HƯỚNG DẪN TẠO FILE CREDENTIALS:")
                    print("1. Vào https://console.cloud.google.com/")
                    print("2. Chọn project → APIs & Services → Credentials")
                    print("3. Create Credentials → OAuth client ID")
                    print("4. Chọn 'Desktop application'")
                    print("5. Tải file JSON và đặt tên 'credentials.json'")
                    print("6. Copy file vào thư mục:", os.getcwd())
                    print("\n💡 Lưu ý: File phải có tên chính xác 'credentials.json'")
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_FILE, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"❌ Lỗi xác thực: {str(e)}")
                    print("\n🔧 KHẮC PHỤC LỖI 400:")
                    print("1. Kiểm tra OAuth consent screen:")
                    print("   - Vào https://console.cloud.google.com/")
                    print("   - APIs & Services → OAuth consent screen")
                    print("   - Đảm bảo app status là 'In production' hoặc 'Testing'")
                    print("   - Nếu 'Testing': Thêm email vào 'Test users'")
                    print("2. Kiểm tra Gmail API đã được bật")
                    print("3. Tạo lại OAuth credentials nếu cần")
                    return False
            
            # Lưu credentials cho lần sau
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Tạo service object
        self.service = build('gmail', 'v1', credentials=self.creds)
        return True
    
    def get_service(self):
        """Trả về Gmail service object"""
        return self.service
