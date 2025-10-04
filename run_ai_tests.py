#!/usr/bin/env python3
"""
Quick AI Testing Launcher
Runs various tests to verify if your AI is working intelligently
"""

import subprocess
import sys
import os

def check_server():
    """Check if the Flask server is running"""
    import requests
    try:
        response = requests.get("http://localhost:5003/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 CREST AI TESTING SUITE")
    print("=" * 50)
    
    # Check if server is running
    if not check_server():
        print("❌ Flask server is not running!")
        print("Please start it first with: python app.py")
        print("Or with Datadog: ddtrace-run python app.py")
        return
    
    print("✅ Flask server is running")
    print()
    
    print("Available tests:")
    print("1. Intelligence Test - Test AI with known loud/quiet subtitles")
    print("2. Decision Monitor - Interactive testing and real-time monitoring")
    print("3. Quick Test - Run a few sample tests")
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Choose a test (1-4): ").strip()
            
            if choice == "1":
                print("\n🧪 Running Intelligence Test...")
                subprocess.run([sys.executable, "test_ai_behavior.py"])
                break
                
            elif choice == "2":
                print("\n🔍 Starting Decision Monitor...")
                subprocess.run([sys.executable, "monitor_ai_decisions.py"])
                break
                
            elif choice == "3":
                print("\n⚡ Running Quick Test...")
                run_quick_test()
                break
                
            elif choice == "4":
                print("Goodbye!")
                break
                
            else:
                print("Please enter 1, 2, 3, or 4")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def run_quick_test():
    """Run a quick test with a few examples"""
    import requests
    import json
    
    test_cases = [
        ("[explosion]", "Should lower volume"),
        ("Hello there", "Should NOT lower volume"),
        ("[gunshot]", "Should lower volume"),
        ("The cat walked quietly", "Should NOT lower volume")
    ]
    
    print("Running quick tests...")
    print()
    
    for subtitle, expected in test_cases:
        print(f"Testing: '{subtitle}' - {expected}")
        
        try:
            response = requests.post(
                "http://localhost:5003/data",
                json={"text": subtitle},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                action = result.get("action", "NONE")
                
                if action == "LOWER_VOLUME":
                    print(f"  🔉 AI Decision: LOWER VOLUME")
                else:
                    print(f"  🔊 AI Decision: NO ACTION")
                    
            else:
                print(f"  ❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    print("Quick test completed!")
    print("\nFor more detailed testing:")
    print("- Run option 1 for full intelligence test")
    print("- Run option 2 for interactive monitoring")
    print("- Use live_youtube_tester.js in browser console for YouTube testing")

if __name__ == "__main__":
    main()