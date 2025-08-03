#!/usr/bin/env python3
"""
Basic test script for SNBit Uploader
This helps debug CI issues and verify core functionality
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly"""
    try:
        import snbit_uploader
        print("✅ Main module import successful")
        
        from snbit_uploader import get_local_ip, format_file_size, is_allowed_file
        print("✅ Core functions import successful")
        
        from snbit_uploader import SNBitRequestHandler
        print("✅ Request handler import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_core_functions():
    """Test core functionality"""
    try:
        from snbit_uploader import get_local_ip, format_file_size, is_allowed_file
        
        # Test IP function
        ip = get_local_ip()
        print(f"✅ Local IP: {ip}")
        
        # Test file size formatting
        size_str = format_file_size(1024)
        assert size_str == "1.0 KB", f"Expected '1.0 KB', got '{size_str}'"
        print(f"✅ File size formatting: {size_str}")
        
        # Test file extension validation
        assert is_allowed_file("test.txt") == True
        assert is_allowed_file("test.exe") == False
        print("✅ File extension validation working")
        
        return True
    except Exception as e:
        print(f"❌ Core function test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    try:
        import snbit_uploader
        
        print(f"✅ Port: {snbit_uploader.PORT}")
        print(f"✅ Max file size: {snbit_uploader.MAX_FILE_SIZE}")
        print(f"✅ Upload dir: {snbit_uploader.UPLOAD_DIR}")
        print(f"✅ Allowed extensions: {len(snbit_uploader.ALLOWED_EXTENSIONS)} types")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 SNBit Uploader - Basic Tests")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("Core Function Tests", test_core_functions),
        ("Configuration Tests", test_configuration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
