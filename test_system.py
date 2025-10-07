#!/usr/bin/env python3
"""
Simple comprehensive test for Crest system
Tests core functionality: subtitle analysis, audio analysis, and basic performance
"""

import requests
import time
import json

BASE_URL = "http://localhost:5003"

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_subtitle_analysis():
    """Test subtitle analysis with key scenarios"""
    print("📝 Testing subtitle analysis...")
    
    test_cases = [
        ("[explosion]", "LOWER_VOLUME"),
        ("[gunshot]", "LOWER_VOLUME"), 
        ("normal conversation", "NONE"),
        ("[thunder]", "LOWER_VOLUME"),
        ("background music", "NONE")
    ]
    
    passed = 0
    for subtitle, expected_action in test_cases:
        try:
            response = requests.post(f"{BASE_URL}/data", json={"text": subtitle}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                actual_action = data.get("action", "NONE")
                
                if actual_action == expected_action:
                    print(f"   ✅ '{subtitle}' -> {actual_action}")
                    passed += 1
                else:
                    print(f"   ❌ '{subtitle}' -> {actual_action} (expected {expected_action})")
            else:
                print(f"   ❌ '{subtitle}' -> HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ '{subtitle}' -> Error: {e}")
    
    print(f"   Result: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)

def test_audio_analysis():
    """Test audio analysis with key scenarios"""
    print("🔊 Testing audio analysis...")
    
    test_cases = [
        # (volume, baseline, spike, expected_action)
        (0.8, 0.2, 0.5, "LOWER_VOLUME"),  # Large spike
        (0.3, 0.25, 0.05, "NONE"),        # Small spike
        (0.9, 0.1, 0.7, "LOWER_VOLUME"),  # Very large spike
    ]
    
    passed = 0
    for volume, baseline, spike, expected_action in test_cases:
        try:
            response = requests.post(f"{BASE_URL}/audio-data", json={
                "volume": volume, "baseline": baseline, "spike": spike
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                actual_action = data.get("action", "NONE")
                
                if actual_action == expected_action:
                    print(f"   ✅ Spike {spike:.2f} -> {actual_action}")
                    passed += 1
                else:
                    print(f"   ❌ Spike {spike:.2f} -> {actual_action} (expected {expected_action})")
            else:
                print(f"   ❌ Spike {spike:.2f} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Spike {spike:.2f} -> Error: {e}")
    
    print(f"   Result: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)

def test_performance():
    """Test basic performance"""
    print("⚡ Testing performance...")
    
    # Test response time
    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/data", json={"text": "[explosion]"}, timeout=5)
        response_time = time.time() - start_time
        
        if response.status_code == 200 and response_time < 2.0:
            print(f"   ✅ Response time: {response_time:.3f}s")
            return True
        else:
            print(f"   ❌ Response time: {response_time:.3f}s (too slow or failed)")
            return False
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CREST SYSTEM TEST")
    print("=" * 30)
    
    # Check server
    if not test_server_health():
        print("❌ Server not running! Start with: python app.py")
        return False
    
    print("✅ Server is running")
    
    # Run tests
    results = []
    results.append(test_subtitle_analysis())
    results.append(test_audio_analysis()) 
    results.append(test_performance())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 RESULTS: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    main()