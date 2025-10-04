#!/usr/bin/env python3
"""
Project Crest Integration Test
Tests the Flask server endpoints and AI integration.
"""

import requests
import json
import time
import os

def test_server_health():
    """Test basic server connectivity"""
    try:
        response = requests.get('http://localhost:5001/data', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('message') == 'Hello':
                print("✅ Server health check passed")
                return True
        print(f"❌ Server health check failed: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_ai_integration():
    """Test AI subtitle analysis"""
    test_cases = [
        {
            'text': '[explosion]',
            'expected': 'LOWER_VOLUME',
            'description': 'Explosion sound effect'
        },
        {
            'text': '[gunshot]',
            'expected': 'LOWER_VOLUME', 
            'description': 'Gunshot sound effect'
        },
        {
            'text': 'Hello, how are you today?',
            'expected': 'MAINTAIN_VOLUME',
            'description': 'Normal conversation'
        },
        {
            'text': '[dramatic music]',
            'expected': 'LOWER_VOLUME',
            'description': 'Dramatic music'
        }
    ]
    
    print("\n🧪 Testing AI Integration...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input: '{test_case['text']}'")
        
        try:
            response = requests.post(
                'http://localhost:5001/data',
                json={'text': test_case['text']},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action')
                confidence = data.get('confidence')
                
                print(f"Response: {action} (AI: {confidence})")
                
                if action == test_case['expected']:
                    print("✅ Test passed")
                else:
                    print(f"❌ Test failed - expected {test_case['expected']}, got {action}")
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        
        # Small delay between requests
        time.sleep(0.5)

def test_cors():
    """Test CORS headers"""
    try:
        response = requests.options('http://localhost:5001/data')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print("✅ CORS enabled")
            return True
        else:
            print("❌ CORS not configured")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Project Crest Integration Tests")
    print("=" * 40)
    
    # Check if server is running
    print("Testing server connectivity...")
    if not test_server_health():
        print("\n❌ Server is not running or not responding")
        print("Start the server with: python start_crest.py")
        return
    
    # Test CORS
    print("\nTesting CORS configuration...")
    test_cors()
    
    # Test AI integration (only if environment variables are set)
    if os.getenv('TRUEFOUNDRY_API_KEY') and os.getenv('TRUEFOUNDRY_BASE_URL'):
        test_ai_integration()
    else:
        print("\n⚠️  Skipping AI tests - TrueFoundry credentials not configured")
        print("Set TRUEFOUNDRY_API_KEY and TRUEFOUNDRY_BASE_URL to test AI integration")
    
    print("\n🎯 Integration test completed!")
    print("\nNext steps:")
    print("1. Load chrome-extension/ in Chrome as unpacked extension")
    print("2. Navigate to YouTube video with captions")
    print("3. Enable closed captions and look for loud sound effects")
    print("4. Verify volume changes when loud captions appear")

if __name__ == "__main__":
    main()