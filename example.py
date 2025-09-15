"""
Ví dụ sử dụng Gmail Tool
"""
from gmail_tool import GmailTool


def example_basic_usage():
    """Ví dụ sử dụng cơ bản"""
    print("=== VÍ DỤ SỬ DỤNG CƠ BẢN ===")
    
    # Khởi tạo tool
    tool = GmailTool()
    if not tool.initialize():
        print("❌ Không thể khởi tạo tool")
        return
    
    # Lấy 50 email mới nhất
    print("\n1. Lấy email mới nhất...")
    emails = tool.fetch_emails(max_results=50)
    
    if emails:
        # Phân tích nội dung
        print("\n2. Phân tích nội dung...")
        analyzed_emails = tool.analyze_emails(emails)
        
        # Hiển thị kết quả
        print("\n3. Hiển thị kết quả...")
        tool.display_emails(analyzed_emails, limit=10)
        
        # Xuất kết quả
        print("\n4. Xuất kết quả...")
        tool.export_results(analyzed_emails, "example_results.txt")


def example_advanced_filtering():
    """Ví dụ lọc nâng cao"""
    print("\n=== VÍ DỤ LỌC NÂNG CAO ===")
    
    tool = GmailTool()
    if not tool.initialize():
        return
    
    # Lấy email từ tháng này
    print("\n1. Lấy email từ tháng này...")
    emails = tool.fetch_emails(max_results=100)
    
    if emails:
        # Lọc email có chứa từ "test" trong tiêu đề
        print("\n2. Lọc email có chứa 'test' trong tiêu đề...")
        filtered_emails = tool.filter_emails(
            emails, 
            subject_contains='test'
        )
        
        if filtered_emails:
            # Phân tích và hiển thị
            analyzed_emails = tool.analyze_emails(filtered_emails)
            tool.display_emails(analyzed_emails)
        else:
            print("Không tìm thấy email nào phù hợp")


def example_search_specific():
    """Ví dụ tìm kiếm cụ thể"""
    print("\n=== VÍ DỤ TÌM KIẾM CỤ THỂ ===")
    
    tool = GmailTool()
    if not tool.initialize():
        return
    
    # Tìm email từ một người cụ thể
    print("\n1. Tìm email từ người gửi cụ thể...")
    emails = tool.fetch_emails(query="from:example@gmail.com")
    
    if emails:
        # Lọc email trong tuần qua
        print("\n2. Lọc email trong tuần qua...")
        from datetime import datetime, timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        filtered_emails = tool.filter_emails(
            emails,
            date_from=week_ago
        )
        
        if filtered_emails:
            analyzed_emails = tool.analyze_emails(filtered_emails)
            tool.display_emails(analyzed_emails)
        else:
            print("Không có email nào trong tuần qua")


def example_custom_keywords():
    """Ví dụ với từ khóa tùy chỉnh"""
    print("\n=== VÍ DỤ VỚI TỪ KHÓA TÙY CHỈNH ===")
    
    tool = GmailTool()
    if not tool.initialize():
        return
    
    # Cập nhật từ khóa phân tích
    tool.analyzer.update_keywords(
        complete_keywords=['success', 'done', 'completed', 'finished'],
        error_keywords=['error', 'failed', 'issue', 'problem']
    )
    
    # Lấy email và phân tích
    emails = tool.fetch_emails(max_results=50)
    if emails:
        analyzed_emails = tool.analyze_emails(emails)
        
        # Hiển thị chỉ email có trạng thái COMPLETE hoặc ERROR
        complete_emails = [e for e in analyzed_emails if e.get('status') == 'COMPLETE']
        error_emails = [e for e in analyzed_emails if e.get('status') == 'ERROR']
        
        print(f"\n📊 Tìm thấy {len(complete_emails)} email COMPLETE và {len(error_emails)} email ERROR")
        
        if complete_emails:
            print("\n✅ EMAIL COMPLETE:")
            tool.display_emails(complete_emails, limit=5)
        
        if error_emails:
            print("\n❌ EMAIL ERROR:")
            tool.display_emails(error_emails, limit=5)


if __name__ == "__main__":
    print("🎯 GMAIL TOOL - VÍ DỤ SỬ DỤNG")
    print("="*50)
    
    try:
        # Chạy các ví dụ
        example_basic_usage()
        example_advanced_filtering()
        example_search_specific()
        example_custom_keywords()
        
        print("\n✅ Hoàn thành tất cả ví dụ!")
        
    except KeyboardInterrupt:
        print("\n👋 Đã dừng chương trình")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("Vui lòng kiểm tra file credentials.json và kết nối internet")
