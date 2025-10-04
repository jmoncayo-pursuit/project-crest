#!/usr/bin/env python3
"""
One-command startup script for Crest AI Demo
Starts server, checks health, and provides next steps
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def print_banner():
    print("🎵" + "="*50)
    print("🚀 CREST AI VOLUME CONTROL DEMO STARTUP")
    print("🎵" + "="*50)

def check_dependencies():
    """Check if required files exist"""
    required_files = [
        "app.py",
        "chrome-extension/manifest.json",
        "chrome-extension/service_worker.js",
        "working_subtle_demo.js"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install Python dependencies if needed"""
    try:
        import flask
        import flask_cors
        print("✅ Python dependencies already installed")
        return True
    except ImportError:
        print("📦 Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

def start_server():
    """Start the Flask server in background"""
    print("🚀 Starting Crest Flask server...")
    
    # Kill any existing server on port 5003
    try:
        subprocess.run(["pkill", "-f", "app.py"], capture_output=True)
        time.sleep(1)
    except:
        pass
    
    # Start server in background
    process = subprocess.Popen([sys.executable, "app.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get("http://localhost:5003/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server started successfully on port 5003")
                return process
        except:
            pass
        time.sleep(1)
        print(f"   Attempt {i+1}/10...")
    
    print("❌ Server failed to start")
    return None

def test_server():
    """Test server endpoints"""
    print("🧪 Testing server endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5003/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️  Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False
    
    # Test AI processing
    try:
        response = requests.post("http://localhost:5003/data", 
                               json={"text": "[explosion]"}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("action") == "LOWER_VOLUME":
                print("✅ AI processing working (detected loud event)")
            else:
                print("⚠️  AI processing working but didn't detect loud event")
        else:
            print(f"⚠️  AI endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ AI processing failed: {e}")
        return False
    
    return True

def show_next_steps():
    """Show what to do next"""
    print("\n🎯 NEXT STEPS FOR DEMO:")
    print("="*50)
    print("1. 📱 LOAD CHROME EXTENSION:")
    print("   • Go to: chrome://extensions/")
    print("   • Enable 'Developer mode' (top right)")
    print("   • Click 'Load unpacked'")
    print("   • Select this project's 'chrome-extension/' folder")
    print()
    print("2. 🎬 TEST ON YOUTUBE:")
    print("   • Go to any YouTube video")
    print("   • Press F12 → Console tab")
    print("   • Look for 'Crest Audio Agent: Script Injected'")
    print()
    print("3. 🎵 RUN DEMO SCRIPT:")
    print("   • In YouTube console, paste this:")
    print("   • Copy from: working_subtle_demo.js")
    print()
    print("4. 🔍 MONITOR ACTIVITY:")
    print("   • Watch console for 'Crest Audio Agent' messages")
    print("   • Check server logs in this terminal")
    print()
    print("🚀 SERVER IS RUNNING - Ready for demo!")
    print("   Press Ctrl+C to stop the server")

def main():
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install Python dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start server
    server_process = start_server()
    if not server_process:
        sys.exit(1)
    
    # Test server
    if not test_server():
        print("⚠️  Server started but some tests failed")
    
    # Show next steps
    show_next_steps()
    
    # Keep server running
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        server_process.terminate()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()