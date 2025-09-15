"""
Script debug để test từ khóa phân tích
"""
from content_analyzer import ContentAnalyzer
from config import PACKAGE_SUCCESS_KEYWORDS, PACKAGE_FAILED_KEYWORDS

# Test với các tiêu đề thực tế từ ảnh
test_subjects = [
    "Fwd: Kim, your package has arrived",
    "Fwd: your Bath & Body Works could not be delivered",
    "Fwd: Kim, your package has arrived -",
    "Fwd: your Bath & Body Works could not be delivered",
]

analyzer = ContentAnalyzer()

print("=== DEBUG TEST ===")
print(f"SUCCESS keywords: {PACKAGE_SUCCESS_KEYWORDS}")
print(f"FAILED keywords: {PACKAGE_FAILED_KEYWORDS}")
print()

for i, subject in enumerate(test_subjects, 1):
    print(f"Test {i}: '{subject}'")
    
    # Tạo email object giả
    test_email = {
        'subject': subject,
        'from': 'test@example.com',
        'body': '',
        'snippet': ''
    }
    
    # Phân tích
    status, confidence = analyzer._analyze_single_email(test_email)
    print(f"   Result: {status} (confidence: {confidence})")
    
    # Kiểm tra từ khóa cụ thể
    subject_lower = subject.lower()
    print(f"   Subject lower: '{subject_lower}'")
    
    for keyword in PACKAGE_SUCCESS_KEYWORDS:
        if keyword.lower() in subject_lower:
            print(f"   ✓ Matched SUCCESS keyword: '{keyword}'")
    
    for keyword in PACKAGE_FAILED_KEYWORDS:
        if keyword.lower() in subject_lower:
            print(f"   ✓ Matched FAILED keyword: '{keyword}'")
    
    print()
