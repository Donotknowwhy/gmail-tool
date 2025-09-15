"""
Test script để kiểm tra trích xuất order number
"""
import re
from content_analyzer import ContentAnalyzer

# Test với nội dung email thực tế từ ảnh
test_email_content = """
Bath & Body Works®
Order Number 00474270370383
Order Date 09/02/2025
Good news...your package is here!
"""

# Tạo email object giả
test_email = {
    'subject': 'Fwd: Kim, your package has arrived',
    'from': 'Nam Huy <namnh11promax@gmail.com>',
    'body': test_email_content,
    'snippet': 'Order Number 00474270370383'
}

analyzer = ContentAnalyzer()

print("=== TEST ORDER EXTRACTION ===")
print(f"Email content: {test_email_content}")
print()

# Test trích xuất order number
order_number = analyzer.extract_order_number(test_email)
print(f"Extracted order number: '{order_number}'")

# Test phân tích trạng thái
status, confidence = analyzer._analyze_single_email(test_email)
print(f"Status: {status} (confidence: {confidence})")

# Test các pattern cụ thể
patterns = [
    r'order\s*number\s*([0-9]+)',
    r'order\s*#?\s*:?\s*([0-9]+)',
    r'order\s*number\s*:?\s*([0-9]+)',
    r'order\s*id\s*:?\s*([0-9]+)',
    r'#([0-9]+)',
    r'order\s*([0-9]+)',
    r'([0-9]{10,})',  # Tìm số có ít nhất 10 chữ số
]

print("\n=== TEST PATTERNS ===")
for i, pattern in enumerate(patterns, 1):
    matches = re.findall(pattern, test_email_content, re.IGNORECASE)
    print(f"Pattern {i}: {pattern}")
    print(f"  Matches: {matches}")
    if matches:
        print(f"  ✓ Found: {matches[0]}")
    print()
