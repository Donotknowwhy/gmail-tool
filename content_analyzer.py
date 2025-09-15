"""
Module phân tích nội dung email và đánh dấu trạng thái
"""
import re
from typing import List, Dict, Tuple
from config import COMPLETE_KEYWORDS, ERROR_KEYWORDS, PACKAGE_SUCCESS_KEYWORDS, PACKAGE_FAILED_KEYWORDS


class ContentAnalyzer:
    def __init__(self, complete_keywords: List[str] = None, error_keywords: List[str] = None):
        """
        Khởi tạo analyzer với các từ khóa tùy chỉnh
        
        Args:
            complete_keywords: Danh sách từ khóa để đánh dấu COMPLETE
            error_keywords: Danh sách từ khóa để đánh dấu ERROR
        """
        self.complete_keywords = complete_keywords or COMPLETE_KEYWORDS
        self.error_keywords = error_keywords or ERROR_KEYWORDS
    
    def analyze_emails(self, emails: List[Dict]) -> List[Dict]:
        """
        Phân tích danh sách email và thêm trạng thái
        
        Args:
            emails: Danh sách email cần phân tích
            
        Returns:
            Danh sách email đã được phân tích với trạng thái
        """
        analyzed_emails = []
        
        for email in emails:
            analyzed_email = email.copy()
            status, confidence = self._analyze_single_email(email)
            
            analyzed_email['status'] = status
            analyzed_email['confidence'] = confidence
            analyzed_email['matched_keywords'] = self._get_matched_keywords(email)
            analyzed_email['order_number'] = self.extract_order_number(email)
            
            analyzed_emails.append(analyzed_email)
        
        return analyzed_emails
    
    def _analyze_single_email(self, email: Dict) -> Tuple[str, float]:
        """
        Phân tích một email và trả về trạng thái
        
        Args:
            email: Email object
            
        Returns:
            Tuple (status, confidence) - trạng thái và độ tin cậy
        """
        # Lấy nội dung để phân tích
        content = self._get_analyze_content(email)
        content_lower = content.lower()
        
        # Kiểm tra tiêu đề thư trước
        subject = email.get('subject', '').lower()
        
        # Debug: In ra tiêu đề để kiểm tra
        print(f"   Debug - Subject: {subject}")
        
        # Kiểm tra từ khóa package delivery (kiểm tra linh hoạt)
        for keyword in PACKAGE_SUCCESS_KEYWORDS:
            keyword_lower = keyword.lower()
            if keyword_lower in subject:
                print(f"   Debug - Matched SUCCESS keyword: '{keyword}' in '{subject}'")
                return "PACKAGE_SUCCESS", 1.0
        
        for keyword in PACKAGE_FAILED_KEYWORDS:
            keyword_lower = keyword.lower()
            if keyword_lower in subject:
                print(f"   Debug - Matched FAILED keyword: '{keyword}' in '{subject}'")
                return "PACKAGE_FAILED", 1.0
        
        # Đếm số từ khóa COMPLETE và ERROR
        complete_count = self._count_keywords(content_lower, self.complete_keywords)
        error_count = self._count_keywords(content_lower, self.error_keywords)
        
        # Xác định trạng thái dựa trên số lượng từ khóa
        if complete_count > 0 and error_count == 0:
            return "COMPLETE", min(complete_count * 0.3, 1.0)
        elif error_count > 0 and complete_count == 0:
            return "ERROR", min(error_count * 0.3, 1.0)
        elif complete_count > 0 and error_count > 0:
            # Nếu có cả hai, ưu tiên theo số lượng
            if complete_count >= error_count:
                return "COMPLETE", min(complete_count * 0.2, 0.8)
            else:
                return "ERROR", min(error_count * 0.2, 0.8)
        else:
            return "UNKNOWN", 0.0
    
    def _get_analyze_content(self, email: Dict) -> str:
        """
        Lấy nội dung để phân tích từ email
        
        Args:
            email: Email object
            
        Returns:
            Nội dung text để phân tích
        """
        # Kết hợp subject, snippet và body
        content_parts = []
        
        if email.get('subject'):
            content_parts.append(email['subject'])
        
        if email.get('snippet'):
            content_parts.append(email['snippet'])
        
        if email.get('body'):
            content_parts.append(email['body'])
        
        content = ' '.join(content_parts)
        
        # Debug: In ra nội dung để kiểm tra
        print(f"   Debug - Content length: {len(content)}")
        if len(content) > 200:
            print(f"   Debug - Content preview: {content[:200]}...")
        else:
            print(f"   Debug - Full content: {content}")
        
        return content
    
    def _count_keywords(self, content: str, keywords: List[str]) -> int:
        """
        Đếm số lượng từ khóa xuất hiện trong nội dung
        
        Args:
            content: Nội dung text
            keywords: Danh sách từ khóa
            
        Returns:
            Số lượng từ khóa tìm thấy
        """
        count = 0
        
        for keyword in keywords:
            # Tìm kiếm không phân biệt hoa thường
            keyword_lower = keyword.lower()
            
            # Đếm số lần xuất hiện
            matches = len(re.findall(re.escape(keyword_lower), content))
            count += matches
        
        return count
    
    def _get_matched_keywords(self, email: Dict) -> Dict[str, List[str]]:
        """
        Lấy danh sách từ khóa đã match
        
        Args:
            email: Email object
            
        Returns:
            Dict chứa các từ khóa đã match
        """
        content = self._get_analyze_content(email)
        content_lower = content.lower()
        
        matched_complete = []
        matched_error = []
        
        # Tìm từ khóa COMPLETE
        for keyword in self.complete_keywords:
            if keyword.lower() in content_lower:
                matched_complete.append(keyword)
        
        # Tìm từ khóa ERROR
        for keyword in self.error_keywords:
            if keyword.lower() in content_lower:
                matched_error.append(keyword)
        
        return {
            'complete': matched_complete,
            'error': matched_error
        }
    
    def get_status_summary(self, analyzed_emails: List[Dict]) -> Dict[str, int]:
        """
        Tạo tóm tắt trạng thái của các email
        
        Args:
            analyzed_emails: Danh sách email đã phân tích
            
        Returns:
            Dict chứa số lượng email theo từng trạng thái
        """
        summary = {
            'COMPLETE': 0,
            'ERROR': 0,
            'PACKAGE_SUCCESS': 0,
            'PACKAGE_FAILED': 0,
            'UNKNOWN': 0,
            'TOTAL': len(analyzed_emails)
        }
        
        for email in analyzed_emails:
            status = email.get('status', 'UNKNOWN')
            if status in summary:
                summary[status] += 1
        
        return summary
    
    def filter_by_status(self, analyzed_emails: List[Dict], status: str) -> List[Dict]:
        """
        Lọc email theo trạng thái
        
        Args:
            analyzed_emails: Danh sách email đã phân tích
            status: Trạng thái cần lọc ('COMPLETE', 'ERROR', 'UNKNOWN')
            
        Returns:
            Danh sách email có trạng thái phù hợp
        """
        return [email for email in analyzed_emails if email.get('status') == status]
    
    def update_keywords(self, complete_keywords: List[str] = None, error_keywords: List[str] = None):
        """
        Cập nhật từ khóa phân tích
        
        Args:
            complete_keywords: Danh sách từ khóa COMPLETE mới
            error_keywords: Danh sách từ khóa ERROR mới
        """
        if complete_keywords is not None:
            self.complete_keywords = complete_keywords
        
        if error_keywords is not None:
            self.error_keywords = error_keywords
    
    def extract_order_number(self, email: Dict) -> str:
        """
        Trích xuất order number từ nội dung email
        
        Args:
            email: Email object
            
        Returns:
            Order number nếu tìm thấy, empty string nếu không
        """
        content = self._get_analyze_content(email)
        
        # Các pattern để tìm order number
        patterns = [
            r'order\s*number\s*([0-9]+)',
            r'order\s*#?\s*:?\s*([0-9]+)',
            r'order\s*number\s*:?\s*([0-9]+)',
            r'order\s*id\s*:?\s*([0-9]+)',
            r'#([0-9]+)',
            r'order\s*([0-9]+)',
            r'([0-9]{10,})',  # Tìm số có ít nhất 10 chữ số
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return ""
