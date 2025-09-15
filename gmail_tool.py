"""
Gmail Tool - Tool chính để truy cập và phân tích email Gmail
"""
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
from tabulate import tabulate
from colorama import init, Fore, Style

from gmail_auth import GmailAuthenticator
from email_fetcher import EmailFetcher
from email_filter import EmailFilter
from content_analyzer import ContentAnalyzer
from config import DEFAULT_MAX_RESULTS

# Khởi tạo colorama
init(autoreset=True)


class GmailTool:
    def __init__(self):
        self.authenticator = GmailAuthenticator()
        self.fetcher = None
        self.filter = EmailFilter()
        self.analyzer = ContentAnalyzer()
        self.service = None
    
    def initialize(self) -> bool:
        """
        Khởi tạo tool và xác thực với Gmail
        
        Returns:
            True nếu khởi tạo thành công, False nếu có lỗi
        """
        print(f"{Fore.CYAN}🚀 Đang khởi tạo Gmail Tool...")
        
        # Xác thực với Gmail
        if not self.authenticator.authenticate():
            print(f"{Fore.RED}❌ Không thể xác thực với Gmail API")
            return False
        
        self.service = self.authenticator.get_service()
        self.fetcher = EmailFetcher(self.service)
        
        print(f"{Fore.GREEN}✅ Khởi tạo thành công!")
        return True
    
    def fetch_emails(self, query: str = '', max_results: int = DEFAULT_MAX_RESULTS) -> List[Dict]:
        """
        Lấy danh sách email từ Gmail
        
        Args:
            query: Query string để lọc email
            max_results: Số lượng email tối đa
            
        Returns:
            Danh sách email
        """
        if not self.fetcher:
            print(f"{Fore.RED}❌ Tool chưa được khởi tạo")
            return []
        
        print(f"{Fore.YELLOW}📧 Đang lấy email từ Gmail...")
        emails = self.fetcher.get_emails(query, max_results)
        
        if emails:
            print(f"{Fore.GREEN}✅ Đã lấy được {len(emails)} email")
        else:
            print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào")
        
        return emails
    
    def filter_emails(self, emails: List[Dict], **filters) -> List[Dict]:
        """
        Lọc email theo các tiêu chí
        
        Args:
            emails: Danh sách email cần lọc
            **filters: Các tiêu chí lọc
            
        Returns:
            Danh sách email đã được lọc
        """
        if not emails:
            return []
        
        print(f"{Fore.YELLOW}🔍 Đang lọc {len(emails)} email...")
        filtered_emails = self.filter.filter_emails(emails, **filters)
        
        print(f"{Fore.GREEN}✅ Đã lọc được {len(filtered_emails)} email phù hợp")
        return filtered_emails
    
    def analyze_emails(self, emails: List[Dict]) -> List[Dict]:
        """
        Phân tích nội dung email và đánh dấu trạng thái
        
        Args:
            emails: Danh sách email cần phân tích
            
        Returns:
            Danh sách email đã được phân tích
        """
        if not emails:
            return []
        
        print(f"{Fore.YELLOW}🔬 Đang phân tích {len(emails)} email...")
        analyzed_emails = self.analyzer.analyze_emails(emails)
        
        # Hiển thị tóm tắt
        summary = self.analyzer.get_status_summary(analyzed_emails)
        self._display_status_summary(summary)
        
        return analyzed_emails
    
    def display_emails(self, emails: List[Dict], show_body: bool = False, limit: int = 20):
        """
        Hiển thị danh sách email
        
        Args:
            emails: Danh sách email cần hiển thị
            show_body: Có hiển thị nội dung email không
            limit: Số lượng email tối đa hiển thị
        """
        if not emails:
            print(f"{Fore.YELLOW}⚠️ Không có email nào để hiển thị")
            return
        
        # Giới hạn số lượng hiển thị
        display_emails = emails[:limit]
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}📋 DANH SÁCH EMAIL ({len(display_emails)}/{len(emails)})")
        print(f"{Fore.CYAN}{'='*80}")
        
        for i, email in enumerate(display_emails, 1):
            self._display_single_email(email, i, show_body)
        
        if len(emails) > limit:
            print(f"\n{Fore.YELLOW}... và {len(emails) - limit} email khác")
    
    def _display_single_email(self, email: Dict, index: int, show_body: bool = False):
        """Hiển thị một email"""
        # Màu sắc theo trạng thái
        status = email.get('status', 'UNKNOWN')
        if status == 'COMPLETE':
            status_color = Fore.GREEN
        elif status == 'ERROR':
            status_color = Fore.RED
        elif status == 'PACKAGE_SUCCESS':
            status_color = Fore.GREEN
        elif status == 'PACKAGE_FAILED':
            status_color = Fore.RED
        else:
            status_color = Fore.YELLOW
        
        print(f"\n{Fore.WHITE}{index}. {email.get('subject', 'Không có tiêu đề')}")
        print(f"   {Fore.BLUE}Từ: {email.get('from', 'Không xác định')}")
        print(f"   {Fore.BLUE}Ngày: {email.get('date', 'Không xác định')}")
        print(f"   {Fore.BLUE}Trạng thái: {status_color}{status}")
        
        # Hiển thị order number nếu có
        order_number = email.get('order_number', '')
        if order_number:
            print(f"   {Fore.CYAN}📦 Order Number: {order_number}")
        
        if email.get('matched_keywords'):
            keywords = email['matched_keywords']
            if keywords.get('complete'):
                print(f"   {Fore.GREEN}✅ Từ khóa COMPLETE: {', '.join(keywords['complete'])}")
            if keywords.get('error'):
                print(f"   {Fore.RED}❌ Từ khóa ERROR: {', '.join(keywords['error'])}")
        
        if show_body and email.get('body'):
            body_preview = email['body'][:200] + "..." if len(email['body']) > 200 else email['body']
            print(f"   {Fore.WHITE}Nội dung: {body_preview}")
    
    def _display_status_summary(self, summary: Dict[str, int]):
        """Hiển thị tóm tắt trạng thái"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}📊 TÓM TẮT TRẠNG THÁI")
        print(f"{Fore.CYAN}{'='*50}")
        
        # Tính tổng COMPLETE (bao gồm cả PACKAGE_SUCCESS)
        complete_total = summary.get('COMPLETE', 0) + summary.get('PACKAGE_SUCCESS', 0)
        # Tính tổng ERROR (bao gồm cả PACKAGE_FAILED)
        error_total = summary.get('ERROR', 0) + summary.get('PACKAGE_FAILED', 0)
        
        print(f"{Fore.GREEN}✅ COMPLETE: {complete_total}")
        print(f"{Fore.RED}❌ ERROR: {error_total}")
        print(f"{Fore.WHITE}📧 TỔNG CỘNG: {summary['TOTAL']}")
    
    def _display_order_numbers(self, emails: List[Dict]):
        """Hiển thị danh sách order number theo trạng thái"""
        complete_orders = []
        error_orders = []
        
        for email in emails:
            order_number = email.get('order_number', '')
            status = email.get('status', '')
            
            if order_number:  # Chỉ hiển thị nếu có order number
                if status in ['COMPLETE', 'PACKAGE_SUCCESS']:
                    complete_orders.append(order_number)
                elif status in ['ERROR', 'PACKAGE_FAILED']:
                    error_orders.append(order_number)
        
        if complete_orders:
            print(f"\n{Fore.GREEN}📦 DANH SÁCH ORDER NUMBER - COMPLETE:")
            for i, order in enumerate(complete_orders, 1):
                print(f"   {i}. {order}")
        
        if error_orders:
            print(f"\n{Fore.RED}📦 DANH SÁCH ORDER NUMBER - ERROR:")
            for i, order in enumerate(error_orders, 1):
                print(f"   {i}. {order}")
        
        if not complete_orders and not error_orders:
            print(f"\n{Fore.YELLOW}⚠️ Không tìm thấy order number nào")
    
    def export_results(self, emails: List[Dict], filename: str = None):
        """
        Xuất kết quả ra file
        
        Args:
            emails: Danh sách email cần xuất
            filename: Tên file (nếu không có sẽ tự động tạo)
        """
        if not emails:
            print(f"{Fore.YELLOW}⚠️ Không có dữ liệu để xuất")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gmail_results_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("GMAIL TOOL - KẾT QUẢ PHÂN TÍCH EMAIL\n")
                f.write("="*50 + "\n\n")
                
                for i, email in enumerate(emails, 1):
                    f.write(f"{i}. {email.get('subject', 'Không có tiêu đề')}\n")
                    f.write(f"   Từ: {email.get('from', 'Không xác định')}\n")
                    f.write(f"   Ngày: {email.get('date', 'Không xác định')}\n")
                    f.write(f"   Trạng thái: {email.get('status', 'UNKNOWN')}\n")
                    
                    # Hiển thị order number nếu có
                    order_number = email.get('order_number', '')
                    if order_number:
                        f.write(f"   Order Number: {order_number}\n")
                    
                    if email.get('matched_keywords'):
                        keywords = email['matched_keywords']
                        if keywords.get('complete'):
                            f.write(f"   Từ khóa COMPLETE: {', '.join(keywords['complete'])}\n")
                        if keywords.get('error'):
                            f.write(f"   Từ khóa ERROR: {', '.join(keywords['error'])}\n")
                    
                    f.write("\n")
            
            print(f"{Fore.GREEN}✅ Đã xuất kết quả ra file: {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Lỗi khi xuất file: {str(e)}")
    
    def run_interactive_mode(self):
        """Chạy chế độ tương tác"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎯 GMAIL TOOL - CHẾ ĐỘ TƯƠNG TÁC")
        print(f"{Fore.CYAN}{'='*60}")
        
        while True:
            print(f"\n{Fore.WHITE}Chọn chức năng:")
            print(f"{Fore.GREEN}1. Phân tích đơn hàng theo khoảng thời gian")
            print(f"{Fore.GREEN}2. Tìm kiếm email theo từ khóa")
            print(f"{Fore.GREEN}3. Xuất kết quả ra file")
            print(f"{Fore.RED}0. Thoát")
            
            choice = input(f"\n{Fore.YELLOW}Nhập lựa chọn (0-3): ").strip()
            
            if choice == '0':
                print(f"{Fore.CYAN}👋 Tạm biệt!")
                break
            elif choice == '1':
                self._handle_analyze_orders_by_date()
            elif choice == '2':
                self._handle_search()
            elif choice == '3':
                self._handle_export()
            else:
                print(f"{Fore.RED}❌ Lựa chọn không hợp lệ")
    
    def _handle_analyze_orders_by_date(self):
        """Xử lý phân tích đơn hàng theo khoảng thời gian"""
        try:
            print(f"\n{Fore.CYAN}📅 PHÂN TÍCH ĐƠN HÀNG THEO KHOẢNG THỜI GIAN")
            print(f"{Fore.CYAN}{'='*50}")
            
            # Nhập ngày bắt đầu (mặc định là 1 tháng trước)
            from datetime import datetime, timedelta
            default_date_from = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
            date_from_input = input(f"{Fore.YELLOW}Nhập ngày bắt đầu (DD/MM/YYYY) [mặc định: {default_date_from}]: ").strip()
            if not date_from_input:
                date_from_input = default_date_from
            
            # Chuyển đổi từ DD/MM/YYYY sang YYYY-MM-DD
            try:
                date_from = datetime.strptime(date_from_input, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng DD/MM/YYYY")
                return
            
            # Nhập ngày kết thúc (mặc định là ngày mai để bao gồm hết thư hôm nay)
            default_date_to = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
            date_to_input = input(f"{Fore.YELLOW}Nhập ngày kết thúc (DD/MM/YYYY) [mặc định: {default_date_to}]: ").strip()
            if not date_to_input:
                date_to_input = default_date_to
            
            # Chuyển đổi từ DD/MM/YYYY sang YYYY-MM-DD
            try:
                date_to = datetime.strptime(date_to_input, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng DD/MM/YYYY")
                return
            
            # Nhập số lượng email tối đa
            max_results = int(input(f"{Fore.YELLOW}Nhập số lượng email tối đa (mặc định 50): ") or "50")
            
            print(f"\n{Fore.YELLOW}🔍 Đang tìm kiếm email từ {date_from} đến {date_to}...")
            
            # Tạo query để tìm tất cả email trong hộp thư đến theo khoảng thời gian
            query = f"after:{date_from} before:{date_to}"
            
            # Lấy email
            emails = self.fetch_emails(query=query, max_results=max_results)
            
            if not emails:
                print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào trong khoảng thời gian này")
                return
            
            # Phân tích email
            print(f"\n{Fore.YELLOW}🔬 Đang phân tích {len(emails)} email...")
            analyzed_emails = self.analyze_emails(emails)
            
            # Lọc chỉ email liên quan đến đơn hàng
            package_emails = []
            for email in analyzed_emails:
                status = email.get('status', '')
                if status in ['PACKAGE_SUCCESS', 'PACKAGE_FAILED']:
                    package_emails.append(email)
            
            if package_emails:
                print(f"\n{Fore.GREEN}📦 Tìm thấy {len(package_emails)} email liên quan đến đơn hàng:")
                self.display_emails(package_emails, show_body=True)
                
                # Hiển thị tóm tắt trạng thái
                summary = self.analyzer.get_status_summary(package_emails)
                self._display_status_summary(summary)
                
                # Hiển thị danh sách order number
                self._display_order_numbers(package_emails)
            else:
                print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào liên quan đến đơn hàng")
                
        except ValueError:
            print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ")
        except Exception as e:
            print(f"{Fore.RED}❌ Lỗi: {str(e)}")
    
    def _handle_search(self):
        """Xử lý tìm kiếm email"""
        query = input(f"{Fore.YELLOW}Nhập từ khóa tìm kiếm: ").strip()
        if query:
            emails = self.fetch_emails(query=query)
            if emails:
                self.display_emails(emails)
        else:
            print(f"{Fore.RED}❌ Vui lòng nhập từ khóa")
    
    def _handle_export(self):
        """Xử lý xuất kết quả"""
        try:
            print(f"\n{Fore.CYAN}📤 XUẤT KẾT QUẢ RA FILE")
            print(f"{Fore.CYAN}{'='*30}")
            
            # Nhập ngày bắt đầu (mặc định là 1 tháng trước)
            from datetime import datetime, timedelta
            default_date_from = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
            date_from_input = input(f"{Fore.YELLOW}Nhập ngày bắt đầu (DD/MM/YYYY) [mặc định: {default_date_from}]: ").strip()
            if not date_from_input:
                date_from_input = default_date_from
            
            # Chuyển đổi từ DD/MM/YYYY sang YYYY-MM-DD
            try:
                date_from = datetime.strptime(date_from_input, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng DD/MM/YYYY")
                return
            
            # Nhập ngày kết thúc (mặc định là ngày mai để bao gồm hết thư hôm nay)
            default_date_to = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
            date_to_input = input(f"{Fore.YELLOW}Nhập ngày kết thúc (DD/MM/YYYY) [mặc định: {default_date_to}]: ").strip()
            if not date_to_input:
                date_to_input = default_date_to
            
            # Chuyển đổi từ DD/MM/YYYY sang YYYY-MM-DD
            try:
                date_to = datetime.strptime(date_to_input, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng DD/MM/YYYY")
                return
            
            # Nhập số lượng email tối đa
            max_results = int(input(f"{Fore.YELLOW}Nhập số lượng email tối đa (mặc định 50): ") or "50")
            
            print(f"\n{Fore.YELLOW}🔍 Đang tìm kiếm email từ {date_from} đến {date_to}...")
            
            # Tạo query để tìm tất cả email trong hộp thư đến theo khoảng thời gian
            query = f"after:{date_from} before:{date_to}"
            
            # Lấy email
            emails = self.fetch_emails(query=query, max_results=max_results)
            
            if not emails:
                print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào trong khoảng thời gian này")
                return
            
            # Phân tích email
            print(f"\n{Fore.YELLOW}🔬 Đang phân tích {len(emails)} email...")
            analyzed_emails = self.analyze_emails(emails)
            
            # Lọc chỉ email liên quan đến đơn hàng
            package_emails = []
            for email in analyzed_emails:
                status = email.get('status', '')
                if status in ['PACKAGE_SUCCESS', 'PACKAGE_FAILED']:
                    package_emails.append(email)
            
            if package_emails:
                # Tạo tên file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"package_orders_{date_from}_to_{date_to}_{timestamp}.txt"
                
                # Xuất kết quả
                self.export_results(package_emails, filename)
                
                # Hiển thị tóm tắt trạng thái
                summary = self.analyzer.get_status_summary(package_emails)
                self._display_status_summary(summary)
                
                # Hiển thị danh sách order number
                self._display_order_numbers(package_emails)
            else:
                print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào liên quan đến đơn hàng")
                
        except ValueError:
            print(f"{Fore.RED}❌ Định dạng ngày không hợp lệ")
        except Exception as e:
            print(f"{Fore.RED}❌ Lỗi: {str(e)}")


def main():
    """Hàm main để chạy tool"""
    tool = GmailTool()
    
    # Khởi tạo tool
    if not tool.initialize():
        sys.exit(1)
    
    # Chạy chế độ tương tác
    tool.run_interactive_mode()


if __name__ == "__main__":
    main()
