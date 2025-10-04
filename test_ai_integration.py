#!/usr/bin/env python3
"""
Test script for AI integration functionality
"""
import os
import sys
import json
import requests
import time

# Set mock environment variables for testing
os.environ['TRUEFOUNDRY_API_KEY'] = 'test-key'
os.environ['TRUEFOUNDRY_BASE_URL'] = 'https://mock-api.example.com'
os.environ['DD_AGENT_HOST'] = 'localhost'
os.environ['DD_SERVICE'] = 'crest-agent'
os.environ['DD_ENV'] = 'test'
os.environ['DD_VERSION'] = '0.1.0'

def test_server_basic():
    """Test basic server functionality"""
    print("🧪 Testing basic server functionality...")
    
    try:
        # Import and test the app
        sys.path.append('.')
        from app import app
        
        with app.test_client() as client:
            # Test GET request
            response = client.get('/data')
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'Hello'
            print("✅ GET /data works")
            
            # Test health endpoint
            response = client.get('/health')
            assert response.status_code == 200
            health_data = response.get_json()
            assert health_data['status'] == 'healthy'
            print("✅ Health check works")
            
            # Test POST with empty data
            response = client.post('/data', json={})
            assert response.status_code == 400
            print("✅ Empty POST validation works")
            
            print("✅ Basic server tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Basic server test failed: {e}")
        return False

def test_ai_integration_mock():
    """Test AI integration with mocked responses"""
    print("\n🧪 Testing AI integration (mocked)...")
    
    try:
        # Mock the OpenAI client to avoid actual API calls
        import unittest.mock
        
        sys.path.append('.')
        from app import app, analyze_subtitle_for_loud_events
        
        # Mock the truefoundry_client
        with unittest.mock.patch('app.truefoundry_client') as mock_client:
            # Mock response for loud event
            mock_response = unittest.mock.MagicMock()
            mock_response.choices[0].message.content = "YES"
            mock_client.chat.completions.create.return_value = mock_response
            
            # Test loud event detection
            result = analyze_subtitle_for_loud_events("[explosion]")
            assert result == "YES"
            print("✅ Loud event detection works")
            
            # Mock response for normal text
            mock_response.choices[0].message.content = "NO"
            result = analyze_subtitle_for_loud_events("Hello there")
            assert result == "NO"
            print("✅ Normal text detection works")
            
            # Test full endpoint with mocked AI
            with app.test_client() as client:
                response = client.post('/data', json={"text": "[gunshot]"})
                assert response.status_code == 200
                data = response.get_json()
                assert data['action'] == 'LOWER_VOLUME'
                assert data['processed'] == True
                print("✅ Full POST endpoint with AI works")
                
        print("✅ AI integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_example_requests():
    """Test example subtitle processing scenarios"""
    print("\n🧪 Testing example subtitle scenarios...")
    
    test_cases = [
        ("[explosion]", "LOWER_VOLUME"),
        ("[gunshot]", "LOWER_VOLUME"), 
        ("[music intensifies]", "LOWER_VOLUME"),
        ("Hello, how are you?", "MAINTAIN_VOLUME"),
        ("The weather is nice today", "MAINTAIN_VOLUME")
    ]
    
    try:
        import unittest.mock
        sys.path.append('.')
        from app import app
        
        with unittest.mock.patch('app.truefoundry_client') as mock_client:
            with app.test_client() as client:
                for subtitle_text, expected_action in test_cases:
                    # Mock appropriate response
                    mock_response = unittest.mock.MagicMock()
                    if expected_action == "LOWER_VOLUME":
                        mock_response.choices[0].message.content = "YES"
                    else:
                        mock_response.choices[0].message.content = "NO"
                    mock_client.chat.completions.create.return_value = mock_response
                    
                    # Test the request
                    response = client.post('/data', json={"text": subtitle_text})
                    assert response.status_code == 200
                    data = response.get_json()
                    assert data['action'] == expected_action
                    print(f"✅ '{subtitle_text}' → {expected_action}")
        
        print("✅ Example scenarios test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Example scenarios test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AI Integration Tests\n")
    
    success = True
    success &= test_server_basic()
    success &= test_ai_integration_mock()
    success &= test_example_requests()
    
    if success:
        print("\n🎉 All tests passed! AI integration is ready.")
        print("\n📋 Next steps:")
        print("1. Set your TRUEFOUNDRY_API_KEY and TRUEFOUNDRY_BASE_URL environment variables")
        print("2. Start the server with: python app.py")
        print("3. Test with: curl -X POST http://localhost:5000/data -H 'Content-Type: application/json' -d '{\"text\": \"[explosion]\"}'")
        print("4. Check Datadog for traces, logs, and metrics")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)