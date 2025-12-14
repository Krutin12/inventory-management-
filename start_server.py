#!/usr/bin/env python3
"""
Startup script for Factory Management System
This script will help you start the server and connect HTML with Python backend
"""

import os
import sys
import subprocess

def check_python():
    """Check if Python is available"""
    try:
        # Try py command first (Windows)
        result = subprocess.run(['py', '--version'], 
                              capture_output=True, text=True)
        print(f"✓ Python found: {result.stdout.strip()}")
        return True
    except Exception as e:
        try:
            # Fallback to sys.executable
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            print(f"✓ Python found: {result.stdout.strip()}")
            return True
        except Exception as e2:
            print(f"✗ Python not found: {e2}")
            return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        result = subprocess.run(['py', '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Requirements installed successfully")
            return True
        else:
            print(f"✗ Failed to install requirements: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def test_connection():
    """Test the connection between HTML and Python"""
    print("\n🧪 Testing connection...")
    try:
        result = subprocess.run([sys.executable, 'test_connection.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("✓ Connection test passed")
            return True
        else:
            print("✗ Connection test failed")
            return False
    except Exception as e:
        print(f"✗ Error running connection test: {e}")
        return False

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Flask server...")
    print("=" * 60)
    print("🏭 Factory Management System")
    print("=" * 60)
    print("🌐 Frontend (HTML): http://localhost:5000")
    print("🔧 API Endpoints: http://localhost:5000/api/*")
    print("📊 Health Check: http://localhost:5000/api/health")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the server
        subprocess.run([sys.executable, 'run.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")

def main():
    """Main function"""
    print("🏭 Factory Management System - Startup")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        print("\n❌ Python not found. Please install Python first.")
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Failed to install requirements.")
        return False
    
    # Test connection
    if not test_connection():
        print("\n❌ Connection test failed.")
        return False
    
    # Start server
    start_server()
    return True

if __name__ == "__main__":
    main()
