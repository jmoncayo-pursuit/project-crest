#!/usr/bin/env python3
"""
Instant AI Intelligence Test
One command that tells you immediately if your AI is working or just random
"""

import requests
import time
import threading
import os
from datetime import datetime

def test_ai_intelligence():
    """Test AI with known cases and return immediate verdict"""
    
    print("🤖 TESTING AI INTELLIGENCE...")
    print("Testing with known loud and quiet events...")
    
    # Quick test cases - should be obvious to any working AI
    test_cases = [
        ("[explosion]", "LOUD"),
        ("[gunshot]", "LOUD"), 
        ("Hello there", "QUIET"),
        ("The cat walked quietly", "QUIET"),
        ("[thunder]", "LOUD"),
        ("She whispered softly", "QUIET"),
        ("[crash]", "LOUD"),
        ("It was peaceful", "QUIET")
    ]
    
    correct = 0
    total = len(test_cases)
    
    for subtitle, expected in test_cases:
        try:
            response = requests.post(
                "http://localhost:5003/data",
                json={"text": subtitle},
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                actual = "LOUD" if result.get("action") == "LOWER_VOLUME" else "QUIET"
                
                if actual == expected:
                    correct += 1
                    print(f"  ✅ '{subtitle}' → {actual}")
                else:
                    print(f"  ❌ '{subtitle}' → {actual} (expected {expected})")
            else:
                print(f"  ❌ '{subtitle}' → ERROR")
                
        except Exception as e:
            print(f"  ❌ '{subtitle}' → ERROR: {e}")
    
    accuracy = (correct / total) * 100
    
    print(f"\n📊 RESULT: {correct}/{total} correct ({accuracy:.0f}%)")
    
    # Immediate verdict
    if accuracy >= 85:
        print("🎉 VERDICT: AI IS WORKING INTELLIGENTLY!")
        print("   Your system is making smart decisions based on content.")
        print("   Volume changes you see are legitimate AI responses.")
        return "INTELLIGENT"
    elif accuracy >= 60:
        print("⚠️  VERDICT: AI IS PARTIALLY WORKING")
        print("   Some intelligent behavior but may have issues.")
        return "PARTIAL"
    else:
        print("❌ VERDICT: AI IS NOT WORKING INTELLIGENTLY")
        print("   This appears to be random behavior, not smart AI.")
        print("   Volume changes are likely just demo oscillation.")
        return "RANDOM"

def check_system_status():
    """Quick system check"""
    
    # Check server
    try:
        response = requests.get("http://localhost:5003/health", timeout=3)
        server_ok = response.status_code == 200
    except:
        server_ok = False
    
    # Check AI config
    has_ai_key = bool(os.getenv('TRUEFOUNDRY_API_KEY'))
    
    # Check extension files
    extension_ok = os.path.exists("chrome-extension/content-script-enhanced.js")
    
    return server_ok, has_ai_key, extension_ok

def run_live_monitoring():
    """Run continuous monitoring in background"""
    
    def monitor():
        test_cases = ["[explosion]", "Hello there", "[gunshot]", "She smiled"]
        
        while True:
            try:
                for subtitle in test_cases:
                    response = requests.post(
                        "http://localhost:5003/data",
                        json={"text": subtitle},
                        timeout=2
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        action = result.get("action", "NONE")
                        
                        if action == "LOWER_VOLUME":
                            print(f"🔉 {datetime.now().strftime('%H:%M:%S')} - AI lowered volume for: '{subtitle}'")
                        
                    time.sleep(2)
                    
            except:
                time.sleep(5)
    
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    return thread

def main():
    print("🚀 CREST AI INSTANT INTELLIGENCE TEST")
    print("=" * 50)
    print("This will tell you immediately if your AI is working or just random.\n")
    
    # 1. Quick system check
    print("🔍 Checking system...")
    server_ok, has_ai_key, extension_ok = check_system_status()
    
    if not server_ok:
        print("❌ PROBLEM: Flask server not running on localhost:5003")
        print("   Start it with: python app.py")
        return
    
    print("✅ Server is running")
    
    if has_ai_key:
        print("✅ AI credentials found (Live Mode)")
    else:
        print("⚠️  No AI credentials (Mock Mode - using rules)")
    
    if extension_ok:
        print("✅ Enhanced extension files ready")
    else:
        print("⚠️  Extension may need updating")
    
    print()
    
    # 2. Test AI intelligence immediately
    verdict = test_ai_intelligence()
    
    print("\n" + "=" * 50)
    
    if verdict == "INTELLIGENT":
        print("🎉 YOUR AI IS WORKING!")
        print("✅ The system is making intelligent decisions")
        print("✅ Volume changes are based on content analysis")
        print("✅ You can trust the AI's behavior")
        
        print("\n🔄 Starting live monitoring...")
        print("Watch for real-time AI decisions below:")
        print("(Press Ctrl+C to stop)")
        
        # Start live monitoring
        monitor_thread = run_live_monitoring()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Monitoring stopped")
            
    elif verdict == "PARTIAL":
        print("⚠️  YOUR AI IS PARTIALLY WORKING")
        print("• Some intelligent behavior detected")
        print("• May need configuration adjustments")
        print("• Check your API keys and server logs")
        
    else:
        print("❌ YOUR AI IS NOT WORKING INTELLIGENTLY")
        print("• Volume changes appear to be random")
        print("• This is likely just demo oscillation")
        print("• Check your server configuration and API keys")
    
    print(f"\n💡 To test in browser:")
    print("1. Load the extension in Chrome")
    print("2. Go to YouTube with subtitles")
    print("3. Look for volume changes only on loud events like [explosion]")

if __name__ == "__main__":
    main()