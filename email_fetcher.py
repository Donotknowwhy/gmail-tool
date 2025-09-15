"""
Module lấy email từ Gmail
"""
import base64
import email
from datetime import datetime
from typing import List, Dict, Optional
from config import DEFAULT_MAX_RESULTS


class EmailFetcher:
    def __init__(self, service):
        self.service = service
    
    def get_emails(self, query: str = '', max_results: int = DEFAULT_MAX_RESULTS) -> List[Dict]:
        """
        Lấy danh sách email từ Gmail
        
        Args:
            query: Query string để lọc email (ví dụ: 'from:example@gmail.com subject:test')
            max_results: Số lượng email tối đa cần lấy
            
        Returns:
            List các email với thông tin cơ bản
        """
        try:
            # Lấy danh sách message IDs
            results = self.service.users().messages().list(
                userId='me', 
                q=query, 
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            print(f"📧 Đang lấy {len(messages)} email...")
            
            for i, message in enumerate(messages):
                try:
                    # Lấy chi tiết từng email
                    msg = self.service.users().messages().get(
                        userId='me', 
                        id=message['id']
                    ).execute()
                    
                    email_data = self._parse_email(msg)
                    emails.append(email_data)
                    
                    # Hiển thị tiến trình
                    if (i + 1) % 10 == 0:
                        print(f"   Đã xử lý {i + 1}/{len(messages)} email...")
                        
                except Exception as e:
                    print(f"⚠️ Lỗi khi lấy email {message['id']}: {str(e)}")
                    continue
            
            print(f"✅ Hoàn thành lấy {len(emails)} email")
            return emails
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách email: {str(e)}")
            return []
    
    def _parse_email(self, msg: Dict) -> Dict:
        """
        Parse thông tin từ Gmail message object
        
        Args:
            msg: Gmail message object
            
        Returns:
            Dict chứa thông tin email đã được parse
        """
        headers = msg['payload'].get('headers', [])
        
        # Tạo dict từ headers để dễ truy cập
        header_dict = {}
        for header in headers:
            header_dict[header['name'].lower()] = header['value']
        
        # Lấy thông tin cơ bản
        email_data = {
            'id': msg['id'],
            'thread_id': msg['threadId'],
            'subject': header_dict.get('subject', ''),
            'from': header_dict.get('from', ''),
            'to': header_dict.get('to', ''),
            'date': header_dict.get('date', ''),
            'timestamp': msg['internalDate'],
            'snippet': msg.get('snippet', ''),
            'body': self._extract_body(msg['payload']),
            'labels': msg.get('labelIds', [])
        }
        
        return email_data
    
    def _extract_body(self, payload: Dict) -> str:
        """
        Trích xuất nội dung email từ payload
        
        Args:
            payload: Email payload object
            
        Returns:
            Nội dung email dưới dạng text
        """
        body = ""
        
        if 'parts' in payload:
            # Email có nhiều phần
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body += base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        # Chỉ lấy text từ HTML nếu không có text/plain
                        if not body:
                            html_content = base64.urlsafe_b64decode(
                                part['body']['data']
                            ).decode('utf-8', errors='ignore')
                            # Loại bỏ HTML tags đơn giản
                            import re
                            body = re.sub(r'<[^>]+>', '', html_content)
        else:
            # Email chỉ có một phần
            if payload['mimeType'] == 'text/plain':
                if 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(
                        payload['body']['data']
                    ).decode('utf-8', errors='ignore')
            elif payload['mimeType'] == 'text/html':
                if 'data' in payload['body']:
                    html_content = base64.urlsafe_b64decode(
                        payload['body']['data']
                    ).decode('utf-8', errors='ignore')
                    import re
                    body = re.sub(r'<[^>]+>', '', html_content)
        
        return body.strip()
    
    def search_emails(self, query: str, max_results: int = DEFAULT_MAX_RESULTS) -> List[Dict]:
        """
        Tìm kiếm email với query cụ thể
        
        Args:
            query: Query string để tìm kiếm
            max_results: Số lượng kết quả tối đa
            
        Returns:
            List các email phù hợp
        """
        return self.get_emails(query, max_results)
