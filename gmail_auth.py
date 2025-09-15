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
                    print("Vui lòng tải file credentials từ Google Cloud Console:")
                    print("1. Truy cập https://console.cloud.google.com/")
                    print("2. Tạo project mới hoặc chọn project hiện có")
                    print("3. Bật Gmail API")
                    print("4. Tạo OAuth 2.0 credentials")
                    print("5. Tải file JSON và đặt tên là 'credentials.json'")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Lưu credentials cho lần sau
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Tạo service object
        self.service = build('gmail', 'v1', credentials=self.creds)
        return True
    
    def get_service(self):
        """Trả về Gmail service object"""
        return self.service
