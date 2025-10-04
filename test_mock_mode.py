#!/usr/bin/env python3
"""
Test script to verify Mock Mode functionality
"""
import requests
import json
import time

def test_mock_mode():
    """Test the server in Mock Mode"""
    print("🧪 Testing Mock Mode Functionality")
    print("=" * 40)
    
    # Test cases for Mock Mode
    test_cases = [
        # Should trigger LOWER_VOLUME
        ("[explosion]", "LOWER_VOLUME"),
        ("[gunshot]", "LOWER_VOLUME"), 
        ("[dramatic music]", "LOWER_VOLUME"),
        ("[thunder]", "LOWER_VOLUME"),
        ("[crash]", "LOWER_VOLUME"),
        ("There was a loud explosion", "LOWER_VOLUME"),
        ("Gunshot in the distance", "LOWER_VOLUME"),
        
        # Should return NONE
        ("Hello there", "NONE"),
        ("The weather is nice", "NONE"),
        ("She walked quietly", "NONE"),
        ("Normal conversation", "NONE"),
        ("[whispering]", "NONE"),
    ]
    
    server_url = "http://localhost:5003/data"
    
    print(f"Testing server at: {server_url}")
    print()
    
    # Test server connectivity first
    try:
        response = requests.get(server_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Start it with: python start_crest.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    print("\n🎯 Testing Mock Mode Logic:")
    print("-" * 30)
    
    success_count = 0
    total_tests = len(test_cases)
    
    for subtitle_text, expected_action in test_cases:
        try:
            # Send POST request with subtitle text
            response = requests.post(
                server_url,
                json={"text": subtitle_text},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                actual_action = data.get('action', 'UNKNOWN')
                confidence = data.get('confidence', 'UNKNOWN')
                
                if actual_action == expected_action:
                    print(f"✅ '{subtitle_text}' → {actual_action} (AI: {confidence})")
                    success_count += 1
                else:
                    print(f"❌ '{subtitle_text}' → {actual_action} (expected {expected_action}, AI: {confidence})")
            else:
                print(f"❌ '{subtitle_text}' → HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ '{subtitle_text}' → Error: {e}")
        
        # Small delay between requests
        time.sleep(0.1)
    
    print("\n📊 Test Results:")
    print(f"   Passed: {success_count}/{total_tests}")
    print(f"   Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("\n🎉 All Mock Mode tests passed!")
        return True
    else:
        print(f"\n⚠️  {total_tests - success_count} tests failed")
        return False

def test_volume_response_format():
    """Test that LOWER_VOLUME responses have the correct format"""
    print("\n🔍 Testing Response Format:")
    print("-" * 25)
    
    try:
        response = requests.post(
            "http://localhost:5003/data",
            json={"text": "[explosion]"},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields for LOWER_VOLUME response
            required_fields = ['action', 'level', 'duration', 'confidence']
            missing_fields = []
            
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if not missing_fields:
                print("✅ Response format is correct:")
                print(f"   Action: {data['action']}")
                print(f"   Level: {data['level']}")
                print(f"   Duration: {data['duration']}ms")
                print(f"   Confidence: {data['confidence']}")
                return True
            else:
                print(f"❌ Missing fields: {missing_fields}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Mock Mode Test Suite")
    print("=" * 50)
    
    # Run tests
    basic_tests_passed = test_mock_mode()
    format_tests_passed = test_volume_response_format()
    
    print("\n" + "=" * 50)
    if basic_tests_passed and format_tests_passed:
        print("🎉 All tests passed! Mock Mode is working correctly.")
        print("\n📋 Next steps:")
        print("1. Load Chrome extension")
        print("2. Test on YouTube with captions")
        print("3. Verify volume control works end-to-end")
    else:
        print("❌ Some tests failed. Check the server logs for details.")