#!/usr/bin/env python3
"""
Test if the live agent is working by monitoring server requests
"""

import subprocess
import time
import requests
import sys

def start_server():
    """Start server and return process"""
    print("🚀 Starting server...")
    
    # Kill existing
    subprocess.run(["pkill", "-f", "app.py"], capture_output=True)
    time.sleep(1)
    
    # Start new
    process = subprocess.Popen([sys.executable, "app.py"])
    
    # Wait for startup
    for i in range(10):
        try:
            response = requests.get("http://localhost:5003/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server running on port 5003")
                return process
        except:
            pass
        time.sleep(1)
    
    print("❌ Server failed to start")
    return None

def monitor_requests():
    """Monitor for incoming requests from extension"""
    print("\n🔍 MONITORING FOR LIVE AGENT ACTIVITY")
    print("="*50)
    print("1. Load extension in Chrome (chrome://extensions/)")
    print("2. Go to YouTube video with subtitles")
    print("3. Watch for requests below...")
    print("\nPress Ctrl+C to stop\n")
    
    request_count = 0
    
    while True:
        try:
            # Check server health (this generates a request)
            response = requests.get("http://localhost:5003/health", timeout=2)
            
            if response.status_code == 200:
                request_count += 1
                
                if request_count % 20 == 1:  # Show status every 20 checks
                    print(f"⏳ Server active - Waiting for extension requests...")
                    print(f"   💡 Go to YouTube and check browser console for 'Crest Audio Agent' messages")
                
            time.sleep(3)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Server error: {e}")
            break

def main():
    print("🎵 CREST LIVE AGENT TEST")
    print("="*30)
    
    # Start server
    server_process = start_server()
    if not server_process:
        sys.exit(1)
    
    try:
        # Monitor for activity
        monitor_requests()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n👋 Stopping server...")
        server_process.terminate()
        print("✅ Done")

if __name__ == "__main__":
    main()