#!/usr/bin/env python3
"""
Manual test script to verify the backend is working
"""
import requests
import json
import os

def test_server_running():
    """Test if server is running and responding"""
    try:
        response = requests.get('http://localhost:5001/data', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Start it with: python start_crest.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def test_ai_integration():
    """Test AI integration with real API calls"""
    test_cases = [
        ("[explosion]", "LOWER_VOLUME"),
        ("[gunshot]", "LOWER_VOLUME"),
        ("Hello there", "MAINTAIN_VOLUME"),
        ("The weather is nice", "MAINTAIN_VOLUME")
    ]
    
    print("\n🧪 Testing AI integration...")
    
    for text, expected_action in test_cases:
        try:
            response = requests.post(
                'http://localhost:5001/data',
                json={"text": text},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                ai_decision = data.get('confidence', 'UNKNOWN')
                
                if action == expected_action:
                    print(f"✅ '{text}' → {action} (AI: {ai_decision})")
                else:
                    print(f"⚠️  '{text}' → {action} (expected {expected_action}, AI: {ai_decision})")
            else:
                print(f"❌ '{text}' → HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ '{text}' → Error: {e}")

def check_environment():
    """Check if required environment variables are set"""
    required_vars = [
        'TRUEFOUNDRY_API_KEY',
        'TRUEFOUNDRY_BASE_URL'
    ]
    
    print("🔍 Checking environment variables...")
    missing = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is missing")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing)}")
        print("Set them with:")
        for var in missing:
            print(f"export {var}='your-value-here'")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Manual Backend Test\n")
    
    # Check environment
    env_ok = check_environment()
    
    # Test server
    server_ok = test_server_running()
    
    if server_ok and env_ok:
        test_ai_integration()
        print("\n🎉 Backend testing complete!")
        print("\n📋 Next steps:")
        print("1. Check Datadog dashboard for traces and metrics")
        print("2. Verify logs are appearing with structured JSON format")
        print("3. Test Chrome extension integration")
    else:
        print("\n❌ Prerequisites not met. Fix the issues above and try again.")