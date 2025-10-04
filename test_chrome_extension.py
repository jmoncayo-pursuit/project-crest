#!/usr/bin/env python3
"""
Test Chrome extension integration - simulates what the extension sends
"""
import requests
import json
import time

def test_extension_flow():
    """Simulate the complete Chrome extension flow"""
    print("🔌 Testing Chrome Extension Integration")
    print("=" * 50)
    
    # Test cases that simulate real YouTube subtitle data
    subtitle_tests = [
        "[explosion]",
        "[gunshot]", 
        "[dramatic music]",
        "[thunder rumbling]",
        "[car crash]",
        "Hello everyone, welcome to my channel",
        "Today we're going to learn about...",
        "The weather is beautiful today",
        "[music playing softly]",
        "[applause]"
    ]
    
    print("Sending subtitle data to server (simulating Chrome extension)...\n")
    
    for i, subtitle in enumerate(subtitle_tests, 1):
        try:
            # This is exactly what the Chrome extension sends
            response = requests.post(
                'http://localhost:5003/data',
                headers={'Content-Type': 'application/json'},
                json={'text': subtitle},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                
                if action == 'LOWER_VOLUME':
                    print(f"🔊 Test {i}: '{subtitle}'")
                    print(f"   → 🔇 VOLUME LOWERED to {int(data.get('level', 0) * 100)}% for {data.get('duration', 0)}ms")
                    print(f"   → 🎯 Icon should flash ACTIVE")
                else:
                    print(f"💬 Test {i}: '{subtitle}'")
                    print(f"   → ✅ Normal volume maintained")
                    
            else:
                print(f"❌ Test {i}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
        
        print()
        time.sleep(0.5)  # Small delay to see results clearly
    
    # Test feedback endpoint (user correction)
    print("Testing user feedback (when user manually adjusts volume)...")
    try:
        response = requests.post(
            'http://localhost:5003/feedback',
            json={'event': 'user_corrected_volume'}
        )
        if response.status_code == 200:
            print("✅ User feedback logged successfully")
        else:
            print(f"❌ Feedback failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Feedback error: {e}")

def main():
    print("🎬 Chrome Extension Flow Test")
    print("This simulates what happens when you watch YouTube with Crest extension")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:5003/health', timeout=3)
        if response.status_code == 200:
            print("✅ Server is running")
            print()
            test_extension_flow()
            
            print("\n🎉 Test Complete!")
            print("\nWhat this means for your Chrome extension:")
            print("- Loud events ([explosion], [gunshot]) → Volume lowered + Icon flashes")
            print("- Normal text → No volume change + Icon stays inactive")
            print("- User corrections → Logged for AI improvement")
            
        else:
            print(f"❌ Server returned {response.status_code}")
            
    except Exception as e:
        print(f"❌ Server not reachable: {e}")
        print("\nPlease start the server first:")
        print("python start_demo.py")

if __name__ == '__main__':
    main()