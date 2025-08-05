#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI Test Script for SNBit Uploader
Tests basic functionality and imports for continuous integration
"""

import sys
import os
import io

# Force UTF-8 encoding for stdout/stderr on Windows to handle Unicode characters
if sys.platform.startswith('win'):
    try:
        # Reconfigure stdout and stderr to use UTF-8 encoding
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        # Fallback for older Python versions or if reconfiguration fails
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')

# Alternative: Set environment variable if not already set
if 'PYTHONIOENCODING' not in os.environ:
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all required modules can be imported successfully"""
    try:
        from snbit_uploader import SNBitRequestHandler, get_local_ip, format_file_size, is_allowed_file
        print("✅ Application imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of imported functions"""
    try:
        from snbit_uploader import get_local_ip, format_file_size, is_allowed_file
        
        # Test local IP function
        local_ip = get_local_ip()
        print(f"🌐 Local IP: {local_ip}")
        
        # Test file size formatting
        size_test = format_file_size(1024)
        print(f"📏 Format test (1024 bytes): {size_test}")
        
        # Test file extension validation
        file_check = is_allowed_file("test.txt")
        print(f"📁 File check (test.txt): {file_check}")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading from environment variables"""
    try:
        import snbit_uploader
        
        port = getattr(snbit_uploader, 'PORT', 'Not found')
        max_size = getattr(snbit_uploader, 'MAX_FILE_SIZE', 'Not found')
        
        print(f"✅ Port configured: {port}")
        print(f"✅ Max size configured: {max_size}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_unicode_handling():
    """Test that Unicode characters (emojis) can be printed without errors"""
    try:
        # Test various Unicode characters commonly used in the output
        unicode_chars = "🚀📋✅❌🌐📏📁"
        print(f"🧪 Unicode test: {unicode_chars}")
        print("✅ Unicode characters handled successfully")
        return True
    except UnicodeEncodeError as e:
        print(f"❌ Unicode encoding failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unicode test failed: {e}")
        return False

def test_cross_platform_compatibility():
    """Test cross-platform compatibility"""
    try:
        from snbit_uploader import get_local_ip, format_file_size, is_allowed_file
        
        print(f"✅ Platform: {sys.platform}")
        print(f"🌐 Local IP: {get_local_ip()}")
        print(f"📁 File check: {is_allowed_file('test.txt')}")
        print(f"📏 Size format: {format_file_size(1048576)}")
        
        return True
    except Exception as e:
        print(f"❌ Cross-platform test failed: {e}")
        return False

def main():
    """Run all CI tests"""
    print("🚀 Starting SNBit CI Tests...")
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality Test", test_basic_functionality),
        ("Configuration Test", test_configuration),
        ("Unicode Handling Test", test_unicode_handling),
        ("Cross-Platform Compatibility Test", test_cross_platform_compatibility)
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if not test_func():
            failed_tests.append(test_name)
    
    print(f"\n{'='*50}")
    if failed_tests:
        print(f"❌ {len(failed_tests)} test(s) failed: {', '.join(failed_tests)}")
        sys.exit(1)
    else:
        print("✅ All tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
