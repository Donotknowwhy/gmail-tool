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
        
        # Kiểm tra xem có cần đăng nhập lại không
        token_file = "token.json"
        if not os.path.exists(token_file):
            print(f"{Fore.YELLOW}⚠️ Không tìm thấy token. Sẽ yêu cầu đăng nhập lại...")
        
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
    
    def _export_order_search_results(self):
        """Xuất kết quả tìm kiếm order number ra file"""
        try:
            from datetime import datetime
            
            # Tạo tên file với timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"order_search_results_{timestamp}.txt"
            
            results = self.last_search_results
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KẾT QUẢ TÌM KIẾM ORDER NUMBERS\n")
                f.write("="*50 + "\n\n")
                f.write(f"Phạm vi tìm kiếm: Tất cả email (mọi lúc)\n")
                f.write(f"Tổng số order tìm kiếm: {len(results['success_orders']) + len(results['failed_orders'])}\n\n")
                
                f.write("ORDER SUCCESS:\n")
                f.write("-" * 20 + "\n")
                if results['success_orders']:
                    total_success_qty = 0
                    for order_data in results['success_orders']:
                        order = order_data['order']
                        quantity = order_data['quantity']
                        if quantity:
                            f.write(f"✅ {order} - qty: {quantity}\n")
                            try:
                                total_success_qty += int(quantity)
                            except ValueError:
                                pass
                        else:
                            f.write(f"✅ {order}\n")
                    if total_success_qty > 0:
                        f.write(f"\n📊 Tổng quantity SUCCESS: {total_success_qty}\n")
                else:
                    f.write("Không có order nào thành công\n")
                
                f.write("\nORDER FAILED:\n")
                f.write("-" * 20 + "\n")
                if results['failed_orders']:
                    total_failed_qty = 0
                    for order_data in results['failed_orders']:
                        order = order_data['order']
                        quantity = order_data['quantity']
                        if quantity:
                            f.write(f"❌ {order} - quantity: {quantity}\n")
                            try:
                                total_failed_qty += int(quantity)
                            except ValueError:
                                pass
                        else:
                            f.write(f"❌ {order}\n")
                    if total_failed_qty > 0:
                        f.write(f"\n📊 Tổng quantity FAILED: {total_failed_qty}\n")
                else:
                    f.write("Không có order nào thất bại\n")
                
                f.write("\nORDER NOT FOUND:\n")
                f.write("-" * 20 + "\n")
                if results.get('not_found_orders'):
                    for order in results['not_found_orders']:
                        f.write(f"🔍 {order}\n")
                else:
                    f.write("Không có order nào không tìm thấy\n")
                
                f.write(f"\nTổng kết:\n")
                f.write(f"- Thành công: {len(results['success_orders'])} orders\n")
                f.write(f"- Thất bại: {len(results['failed_orders'])} orders\n")
                f.write(f"- Không tìm thấy: {len(results.get('not_found_orders', []))} orders\n")
            
            print(f"{Fore.GREEN}✅ Đã xuất kết quả tìm kiếm order ra file: {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Lỗi khi xuất file: {str(e)}")
    
    def run_interactive_mode(self):
        """Chạy chế độ tương tác"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🎯 GMAIL TOOL - CHẾ ĐỘ TƯƠNG TÁC")
        print(f"{Fore.CYAN}{'='*60}")
        
        while True:
            print(f"\n{Fore.WHITE}Chọn chức năng:")
            print(f"{Fore.GREEN}1. Tìm kiếm đơn hàng theo order number")
            print(f"{Fore.GREEN}2. Xuất kết quả ra file")
            print(f"{Fore.CYAN}3. Xem 10 email mới nhất")
            print(f"{Fore.YELLOW}4. Đổi tài khoản Google (xóa token)")
            print(f"{Fore.RED}0. Thoát")
            
            choice = input(f"\n{Fore.YELLOW}Nhập lựa chọn (0-4): ").strip()
            
            if choice == '0':
                print(f"{Fore.CYAN}👋 Tạm biệt!")
                break
            elif choice == '1':
                self._handle_search_orders_by_number()
            elif choice == '2':
                self._handle_export()
            elif choice == '3':
                self._handle_view_latest_emails()
            elif choice == '4':
                self._handle_change_account()
            else:
                print(f"{Fore.RED}❌ Lựa chọn không hợp lệ")
    
    def _handle_search_orders_by_number(self):
        """Xử lý tìm kiếm đơn hàng theo order number từ file"""
        # Kiểm tra và khởi tạo lại nếu cần
        if not self.service or not self.fetcher:
            if not self.initialize():
                return
        
        # Mặc định tìm kiếm tất cả email (mọi lúc)
        date_from = "mọi lúc"
        date_to = "mọi lúc"
        date_range_text = "tất cả email (mọi lúc)"
        query_template = "{order_number}"
        
        # Đọc order numbers từ file
        try:
            with open('order_numbers.txt', 'r', encoding='utf-8') as f:
                order_numbers = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Không tìm thấy file order_numbers.txt")
            return
        
        print(f"\n{Fore.CYAN}🔍 Đang tìm kiếm {len(order_numbers)} order numbers trong tất cả email...")
        
        # Tìm kiếm và phân tích từng order number
        success_orders = []  # List of dicts: {'order': 'xxx', 'quantity': 'yy'}
        failed_orders = []   # List of dicts: {'order': 'xxx', 'quantity': 'yy'}
        not_found_orders = []
        
        for i, order_number in enumerate(order_numbers, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(order_numbers)}] Đang tìm kiếm order: {order_number}")
            
            # Tìm kiếm email chứa order number
            query = query_template.format(order_number=order_number)
            emails = self.fetcher.get_emails(query=query, max_results=10)
            
            if not emails:
                print(f"   {Fore.RED}❌ Không tìm thấy email cho order {order_number}")
                not_found_orders.append(order_number)
                continue
            
            # Phân tích email
            analyzer = ContentAnalyzer()
            analyzed_emails = analyzer.analyze_emails(emails)
            
            # Kiểm tra kết quả phân tích
            found_success = False
            found_failed = False
            order_quantity = ""
            
            for email in analyzed_emails:
                status = email.get('status', '')
                quantity = email.get('quantity', '')
                
                if status == 'PACKAGE_SUCCESS':
                    found_success = True
                    order_quantity = quantity
                    print(f"   {Fore.GREEN}✅ Tìm thấy SUCCESS cho order {order_number}")
                    if quantity:
                        print(f"   {Fore.CYAN}📦 Quantity: {quantity}")
                    break
                elif status == 'PACKAGE_FAILED':
                    found_failed = True
                    order_quantity = quantity
                    print(f"   {Fore.RED}❌ Tìm thấy FAILED cho order {order_number}")
                    if quantity:
                        print(f"   {Fore.CYAN}📦 Quantity: {quantity}")
                    break
            
            if found_success:
                success_orders.append({'order': order_number, 'quantity': order_quantity})
            elif found_failed:
                failed_orders.append({'order': order_number, 'quantity': order_quantity})
            else:
                print(f"   {Fore.YELLOW}⚠️ Không xác định được trạng thái cho order {order_number}")
                not_found_orders.append(order_number)
        
        # Hiển thị kết quả tổng hợp
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}📊 KẾT QUẢ TÌM KIẾM ORDER NUMBERS")
        print(f"{Fore.CYAN}{'='*60}")
        
        print(f"\n{Fore.GREEN}✅ ORDER SUCCESS ({len(success_orders)}):")
        if success_orders:
            total_success_qty = 0
            for order_data in success_orders:
                order = order_data['order']
                quantity = order_data['quantity']
                if quantity:
                    print(f"   {Fore.GREEN}• {order} - qty: {quantity}")
                    try:
                        total_success_qty += int(quantity)
                    except ValueError:
                        pass
                else:
                    print(f"   {Fore.GREEN}• {order}")
            if total_success_qty > 0:
                print(f"   {Fore.CYAN}📊 Tổng quantity SUCCESS: {total_success_qty}")
        else:
            print(f"   {Fore.YELLOW}Không có order nào thành công")
        
        print(f"\n{Fore.RED}❌ ORDER FAILED ({len(failed_orders)}):")
        if failed_orders:
            total_failed_qty = 0
            for order_data in failed_orders:
                order = order_data['order']
                quantity = order_data['quantity']
                if quantity:
                    print(f"   {Fore.RED}• {order} - quantity: {quantity}")
                    try:
                        total_failed_qty += int(quantity)
                    except ValueError:
                        pass
                else:
                    print(f"   {Fore.RED}• {order}")
            if total_failed_qty > 0:
                print(f"   {Fore.CYAN}📊 Tổng quantity FAILED: {total_failed_qty}")
        else:
            print(f"   {Fore.YELLOW}Không có order nào thất bại")
        
        print(f"\n{Fore.YELLOW}🔍 ORDER NOT FOUND ({len(not_found_orders)}):")
        if not_found_orders:
            for order in not_found_orders:
                print(f"   {Fore.YELLOW}• {order}")
        else:
            print(f"   {Fore.YELLOW}Không có order nào không tìm thấy")
        
        print(f"\n{Fore.CYAN}📈 Tổng cộng: {len(success_orders)} thành công, {len(failed_orders)} thất bại, {len(not_found_orders)} không tìm thấy")
        
        # Lưu kết quả vào instance để có thể export
        self.last_search_results = {
            'success_orders': success_orders,
            'failed_orders': failed_orders,
            'not_found_orders': not_found_orders,
            'date_from': date_from,
            'date_to': date_to
        }

    def _handle_analyze_orders_by_date(self):
        """Xử lý phân tích đơn hàng theo khoảng thời gian"""
        # Kiểm tra và khởi tạo lại nếu cần
        if not self.service or not self.fetcher:
            if not self.initialize():
                return
        
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
        # Kiểm tra và khởi tạo lại nếu cần
        if not self.service or not self.fetcher:
            if not self.initialize():
                return
        
        query = input(f"{Fore.YELLOW}Nhập từ khóa tìm kiếm: ").strip()
        if query:
            emails = self.fetch_emails(query=query)
            if emails:
                self.display_emails(emails)
        else:
            print(f"{Fore.RED}❌ Vui lòng nhập từ khóa")
    
    def _handle_export(self):
        """Xử lý xuất kết quả"""
        # Kiểm tra xem có kết quả từ tìm kiếm order number không
        if hasattr(self, 'last_search_results') and self.last_search_results:
            self._export_order_search_results()
            return
        
        # Kiểm tra và khởi tạo lại nếu cần
        if not self.service or not self.fetcher:
            if not self.initialize():
                return
        
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
    
    def _handle_view_latest_emails(self):
        """Xử lý xem 10 email mới nhất"""
        # Kiểm tra và khởi tạo lại nếu cần
        if not self.service or not self.fetcher:
            if not self.initialize():
                return
        
        print(f"\n{Fore.CYAN}📧 XEM 10 EMAIL MỚI NHẤT")
        print(f"{Fore.CYAN}{'='*40}")
        
        try:
            # Lấy 10 email mới nhất (tất cả email)
            print(f"{Fore.YELLOW}🔍 Đang lấy 10 email mới nhất...")
            emails = self.fetcher.get_emails(query='', max_results=10)
            
            if not emails:
                print(f"{Fore.YELLOW}⚠️ Không tìm thấy email nào")
                return
            
            # Hiển thị danh sách email
            print(f"\n{Fore.GREEN}✅ Đã lấy được {len(emails)} email mới nhất:")
            self.display_emails(emails, show_body=False, limit=10)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Lỗi khi lấy email: {str(e)}")

    def _handle_change_account(self):
        """Xử lý đổi tài khoản Google bằng cách xóa token"""
        print(f"\n{Fore.CYAN}🔄 ĐỔI TÀI KHOẢN GOOGLE")
        print(f"{Fore.CYAN}{'='*40}")
        
        # Kiểm tra xem có file token.json không
        token_file = "token.json"
        if os.path.exists(token_file):
            print(f"{Fore.YELLOW}📁 Tìm thấy file token hiện tại: {token_file}")
            
            # Xác nhận từ người dùng
            confirm = input(f"{Fore.YELLOW}Bạn có chắc chắn muốn xóa token và đăng nhập lại? (y/n): ").strip().lower()
            
            if confirm in ['y', 'yes', 'có']:
                try:
                    # Xóa file token
                    os.remove(token_file)
                    print(f"{Fore.GREEN}✅ Đã xóa file token thành công!")
                    
                    # Thông báo hướng dẫn
                    print(f"\n{Fore.CYAN}📋 HƯỚNG DẪN:")
                    print(f"{Fore.WHITE}1. Tool sẽ tự động khởi tạo lại khi bạn chọn chức năng khác")
                    print(f"{Fore.WHITE}2. Trình duyệt sẽ mở để bạn chọn Google account mới")
                    print(f"{Fore.WHITE}3. Cấp quyền truy cập email cho tool")
                    print(f"{Fore.WHITE}4. Token mới sẽ được lưu tự động")
                    
                    # Reset authenticator để chuẩn bị cho lần đăng nhập mới
                    self.authenticator = GmailAuthenticator()
                    self.service = None
                    self.fetcher = None
                    
                    print(f"\n{Fore.GREEN}🎉 Hoàn tất! Token đã được xóa.")
                    print(f"{Fore.YELLOW}💡 Lần tiếp theo bạn sử dụng tool, sẽ được yêu cầu đăng nhập lại.")
                    
                except Exception as e:
                    print(f"{Fore.RED}❌ Lỗi khi xóa token: {str(e)}")
            else:
                print(f"{Fore.YELLOW}⚠️ Hủy bỏ thao tác")
        else:
            print(f"{Fore.YELLOW}⚠️ Không tìm thấy file token.json")
            print(f"{Fore.WHITE}Tool sẽ tự động yêu cầu đăng nhập khi cần thiết.")


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
