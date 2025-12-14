#!/usr/bin/env python3
"""
Start the simplified Factory Management System
This version works without database issues
"""

import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    """Start the simplified server"""
    print("🏭 Factory Management System - Simplified Version")
    print("=" * 60)
    print("🚀 Starting server...")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🔧 API health check: http://localhost:5000/api/health")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the simplified server
        subprocess.run([sys.executable, 'simple_app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    main()
