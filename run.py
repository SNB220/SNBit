#!/usr/bin/env python3
"""
SNBit Uploader Launcher Script
Simple script to start the SNBit Uploader with easy configuration
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from snbit_uploader import main
    
    if __name__ == "__main__":
        print("🚀 Starting SNBit Uploader...")
        main()
        
except ImportError as e:
    print(f"❌ Error importing SNBit Uploader: {e}")
    print("📦 Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n⏹️  SNBit Uploader stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
