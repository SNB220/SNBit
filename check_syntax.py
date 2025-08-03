#!/usr/bin/env python3
"""
Syntax check script for SNBit Uploader
"""
import ast
import sys

def check_python_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the content
        ast.parse(content)
        print(f"✅ Syntax check passed for {filepath}")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Python syntax...")
    
    files_to_check = [
        "src/snbit_uploader.py",
        "test_basic.py"
    ]
    
    all_good = True
    for filepath in files_to_check:
        if not check_python_syntax(filepath):
            all_good = False
    
    if all_good:
        print("\n🎉 All files have valid syntax!")
        sys.exit(0)
    else:
        print("\n❌ Syntax errors found!")
        sys.exit(1)
