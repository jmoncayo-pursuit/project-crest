#!/usr/bin/env python3
"""
Complete system test for Crest - tests server, AI, and Chrome extension integration
"""
import requests
import json
import time
import subprocess
import sys
import os

def test_server_health():
    """Test if server is running and healthy"""
    try:
        response = requests.get('http://localhost:5003/health', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not reachable: {e}")
        return False

def test_ai_processing():
    """Test AI processing with different types of subtitle text"""
    test_cases = [
        {
            "text": "[explosion]",
            "expected_action": "LOWER_VOLUME",
            "description": "Loud event - explosion"
        },
        {
            "text": "[gunshot]", 
            "expected_action": "LOWER_VOLUME",
            "description": "Loud event - gunshot"
        },
        {
            "text": "[dramatic music]",
            "expected_action": "LOWER_VOLUME", 
            "description": "Loud event - dramatic music"
        },
        {
            "text": "Hello, how are you?",
            "expected_action": "NONE",
            "description": "Normal conversation"
        },
        {
            "text": "The weather is nice today.",
            "expected_action": "NONE",
            "description": "Normal narration"
        }
    ]
    
    print("\n🧠 Testing AI Processing:")
    print("=" * 50)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                'http://localhost:5003/data',
                json={'text': test_case['text']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                
                if action == test_case['expected_action']:
                    print(f"✅ Test {i}: {test_case['description']}")
                    print(f"   Input: '{test_case['text']}'")
                    print(f"   Action: {action}")
                    if action == "LOWER_VOLUME":
                        print(f"   Volume: {data.get('level', 'N/A')}")
                        print(f"   Duration: {data.get('duration', 'N/A')}ms")
                else:
                    print(f"❌ Test {i}: {test_case['description']}")
                    print(f"   Expected: {test_case['expected_action']}, Got: {action}")
                    all_passed = False
            else:
                print(f"❌ Test {i}: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_chrome_extension_endpoints():
    """Test endpoints that Chrome extension uses"""
    print("🔌 Testing Chrome Extension Endpoints:")
    print("=" * 50)
    
    # Test feedback endpoint
    try:
        response = requests.post('http://localhost:5003/feedback', 
                               json={'event': 'user_corrected_volume'})
        if response.status_code == 200:
            print("✅ Feedback endpoint working")
        else:
            print(f"❌ Feedback endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Feedback endpoint error: {e}")

def check_environment():
    """Check if all required environment variables are set"""
    print("🔧 Checking Environment:")
    print("=" * 50)
    
    required_vars = [
        'TRUEFOUNDRY_API_KEY',
        'TRUEFOUNDRY_BASE_URL', 
        'DD_SERVICE',
        'DD_API_KEY'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask API keys for security
            if 'KEY' in var:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            all_set = False
    
    return all_set

def main():
    print("🚀 Crest System Test")
    print("=" * 60)
    
    # Check environment
    env_ok = check_environment()
    print()
    
    # Test server health
    server_ok = test_server_health()
    print()
    
    if not server_ok:
        print("❌ Server is not running. Please start it first:")
        print("   python app.py")
        return False
    
    # Test AI processing
    ai_ok = test_ai_processing()
    
    # Test Chrome extension endpoints
    test_chrome_extension_endpoints()
    print()
    
    # Summary
    print("📊 Test Summary:")
    print("=" * 50)
    print(f"Environment: {'✅ OK' if env_ok else '❌ Issues'}")
    print(f"Server: {'✅ OK' if server_ok else '❌ Issues'}")
    print(f"AI Processing: {'✅ OK' if ai_ok else '❌ Issues'}")
    
    if env_ok and server_ok and ai_ok:
        print("\n🎉 All systems working! Your Crest agent is ready for the hackathon demo!")
        print("\nNext steps:")
        print("1. Load the Chrome extension from chrome-extension/ folder")
        print("2. Go to a YouTube video with captions")
        print("3. Watch for volume changes and icon flashing")
        return True
    else:
        print("\n⚠️  Some issues found. Please fix them before demo.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)