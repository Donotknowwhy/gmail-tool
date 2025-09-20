#!/usr/bin/env python3
"""
Script test chức năng tìm kiếm order number
"""

import os
from datetime import datetime, timedelta
from gmail_tool import GmailTool

def test_order_search():
    """Test chức năng tìm kiếm order number"""
    print("🧪 TEST CHỨC NĂNG TÌM KIẾM ORDER NUMBER")
    print("=" * 50)
    
    # Khởi tạo Gmail Tool
    tool = GmailTool()
    
    # Kiểm tra file order_numbers.txt
    if not os.path.exists('order_numbers.txt'):
        print("❌ Không tìm thấy file order_numbers.txt")
        return
    
    # Đọc order numbers
    with open('order_numbers.txt', 'r', encoding='utf-8') as f:
        order_numbers = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"📋 Đã đọc {len(order_numbers)} order numbers từ file:")
    for i, order in enumerate(order_numbers, 1):
        print(f"   {i:2d}. {order}")
    
    # Test với ngày mặc định
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    date_to = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"\n📅 Khoảng thời gian test: {date_from} đến {date_to}")
    
    # Test tìm kiếm 3 order đầu tiên
    test_orders = order_numbers[:3]
    print(f"\n🔍 Test tìm kiếm {len(test_orders)} order đầu tiên:")
    
    success_orders = []
    failed_orders = []
    
    for i, order_number in enumerate(test_orders, 1):
        print(f"\n[{i}/{len(test_orders)}] Đang test order: {order_number}")
        
        try:
            # Tạo query tìm kiếm
            query = f"after:{date_from} before:{date_to} {order_number}"
            print(f"   Query: {query}")
            
            # Giả lập kết quả (vì không có Gmail API trong test)
            print(f"   ✅ Order {order_number} - SIMULATED SUCCESS")
            success_orders.append(order_number)
            
        except Exception as e:
            print(f"   ❌ Lỗi: {str(e)}")
    
    # Hiển thị kết quả
    print(f"\n📊 KẾT QUẢ TEST:")
    print(f"✅ ORDER SUCCESS ({len(success_orders)}):")
    for order in success_orders:
        print(f"   • {order}")
    
    print(f"\n❌ ORDER FAILED ({len(failed_orders)}):")
    for order in failed_orders:
        print(f"   • {order}")
    
    print(f"\n🎉 Test hoàn thành!")

if __name__ == "__main__":
    test_order_search()
