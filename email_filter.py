"""
Module lọc email theo các tiêu chí khác nhau
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dateutil import parser


class EmailFilter:
    def __init__(self):
        pass
    
    def filter_emails(self, emails: List[Dict], **filters) -> List[Dict]:
        """
        Lọc danh sách email theo các tiêu chí
        
        Args:
            emails: Danh sách email cần lọc
            **filters: Các tiêu chí lọc (date_from, date_to, month, year, subject_contains, etc.)
            
        Returns:
            Danh sách email đã được lọc
        """
        filtered_emails = emails.copy()
        
        # Lọc theo ngày
        if 'date_from' in filters:
            filtered_emails = self._filter_by_date_from(filtered_emails, filters['date_from'])
        
        if 'date_to' in filters:
            filtered_emails = self._filter_by_date_to(filtered_emails, filters['date_to'])
        
        # Lọc theo tháng
        if 'month' in filters:
            filtered_emails = self._filter_by_month(filtered_emails, filters['month'])
        
        # Lọc theo năm
        if 'year' in filters:
            filtered_emails = self._filter_by_year(filtered_emails, filters['year'])
        
        # Lọc theo tiêu đề
        if 'subject_contains' in filters:
            filtered_emails = self._filter_by_subject(filtered_emails, filters['subject_contains'])
        
        # Lọc theo người gửi
        if 'from_contains' in filters:
            filtered_emails = self._filter_by_sender(filtered_emails, filters['from_contains'])
        
        # Lọc theo nội dung
        if 'body_contains' in filters:
            filtered_emails = self._filter_by_body(filtered_emails, filters['body_contains'])
        
        return filtered_emails
    
    def _filter_by_date_from(self, emails: List[Dict], date_from: str) -> List[Dict]:
        """Lọc email từ ngày cụ thể"""
        try:
            target_date = parser.parse(date_from).date()
            filtered = []
            
            for email in emails:
                email_date = self._parse_email_date(email['date'])
                if email_date and email_date >= target_date:
                    filtered.append(email)
            
            return filtered
        except Exception as e:
            print(f"⚠️ Lỗi khi lọc theo ngày từ: {str(e)}")
            return emails
    
    def _filter_by_date_to(self, emails: List[Dict], date_to: str) -> List[Dict]:
        """Lọc email đến ngày cụ thể"""
        try:
            target_date = parser.parse(date_to).date()
            filtered = []
            
            for email in emails:
                email_date = self._parse_email_date(email['date'])
                if email_date and email_date <= target_date:
                    filtered.append(email)
            
            return filtered
        except Exception as e:
            print(f"⚠️ Lỗi khi lọc theo ngày đến: {str(e)}")
            return emails
    
    def _filter_by_month(self, emails: List[Dict], month: int) -> List[Dict]:
        """Lọc email theo tháng"""
        filtered = []
        
        for email in emails:
            email_date = self._parse_email_date(email['date'])
            if email_date and email_date.month == month:
                filtered.append(email)
        
        return filtered
    
    def _filter_by_year(self, emails: List[Dict], year: int) -> List[Dict]:
        """Lọc email theo năm"""
        filtered = []
        
        for email in emails:
            email_date = self._parse_email_date(email['date'])
            if email_date and email_date.year == year:
                filtered.append(email)
        
        return filtered
    
    def _filter_by_subject(self, emails: List[Dict], subject_keyword: str) -> List[Dict]:
        """Lọc email theo từ khóa trong tiêu đề"""
        filtered = []
        keyword_lower = subject_keyword.lower()
        
        for email in emails:
            subject_lower = email['subject'].lower()
            if keyword_lower in subject_lower:
                filtered.append(email)
        
        return filtered
    
    def _filter_by_sender(self, emails: List[Dict], sender_keyword: str) -> List[Dict]:
        """Lọc email theo từ khóa trong người gửi"""
        filtered = []
        keyword_lower = sender_keyword.lower()
        
        for email in emails:
            from_lower = email['from'].lower()
            if keyword_lower in from_lower:
                filtered.append(email)
        
        return filtered
    
    def _filter_by_body(self, emails: List[Dict], body_keyword: str) -> List[Dict]:
        """Lọc email theo từ khóa trong nội dung"""
        filtered = []
        keyword_lower = body_keyword.lower()
        
        for email in emails:
            body_lower = email['body'].lower()
            if keyword_lower in body_lower:
                filtered.append(email)
        
        return filtered
    
    def _parse_email_date(self, date_str: str) -> Optional[datetime]:
        """Parse ngày từ string"""
        try:
            if not date_str:
                return None
            
            # Thử parse với dateutil
            parsed_date = parser.parse(date_str)
            return parsed_date.date()
        except Exception:
            return None
    
    def build_gmail_query(self, **filters) -> str:
        """
        Xây dựng Gmail query string từ các filter
        
        Args:
            **filters: Các tiêu chí lọc
            
        Returns:
            Gmail query string
        """
        query_parts = []
        
        # Lọc theo ngày
        if 'date_from' in filters:
            query_parts.append(f"after:{filters['date_from']}")
        
        if 'date_to' in filters:
            query_parts.append(f"before:{filters['date_to']}")
        
        # Lọc theo người gửi
        if 'from_contains' in filters:
            query_parts.append(f"from:{filters['from_contains']}")
        
        # Lọc theo tiêu đề
        if 'subject_contains' in filters:
            query_parts.append(f"subject:{filters['subject_contains']}")
        
        # Lọc theo nội dung
        if 'body_contains' in filters:
            query_parts.append(f"{filters['body_contains']}")
        
        return ' '.join(query_parts)
