#!/usr/bin/env python3
"""
Script chạy Gmail Tool với input tự động để test
"""

import sys
import io
from unittest.mock import patch
from gmail_tool import GmailTool

def run_gmail_tool_with_input():
    """Chạy Gmail Tool với input tự động"""
    
    print("🚀 CHẠY GMAIL TOOL VỚI INPUT TỰ ĐỘNG")
    print("=" * 50)
    print("Input sẽ được tự động nhập:")
    print("1. Chọn option 1 (Tìm kiếm đơn hàng)")
    print("2. Chọn lọc theo ngày (1)")
    print("3. Ngày bắt đầu: 01/08/2025")
    print("4. Ngày kết thúc: 21/09/2025") 
    print("5. Thoát (0)")
    print("=" * 50)
    
    # Tạo Gmail Tool
    tool = GmailTool()
    
    # Mock input để nhập tự động
    inputs = ["1", "1", "01/08/2025", "21/09/2025", "0"]
    input_iter = iter(inputs)
    
    def mock_input(prompt=""):
        try:
            value = next(input_iter)
            print(f"{prompt}{value}")
            return value
        except StopIteration:
            return "0"
    
    try:
        with patch('builtins.input', side_effect=mock_input):
            tool.run_interactive_mode()
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\n✅ Hoàn thành test với input tự động!")

if __name__ == "__main__":
    run_gmail_tool_with_input()
