#!/usr/bin/env python3
"""
Start the Factory Management System
"""

import sys
import subprocess

def main():
    """Start the factory management system"""
    print("=" * 60)
    print("Factory Management System")
    print("=" * 60)
    print("Starting server...")
    print("Frontend: http://localhost:5000")
    print("Login credentials:")
    print("  Admin: username=admin, password=password")
    print("  Manager: username=manager, password=password")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the working server
        subprocess.run([sys.executable, 'run_working.py'])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")

if __name__ == "__main__":
    main()
