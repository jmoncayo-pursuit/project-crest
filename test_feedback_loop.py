#!/usr/bin/env python3
"""
Test script to verify the feedback loop functionality
"""
import requests
import json
import time

def test_feedback_endpoint():
    """Test the new /feedback endpoint"""
    print("🔄 Testing Feedback Loop Functionality")
    print("=" * 40)
    
    server_url = "http://localhost:5003/feedback"
    
    print(f"Testing feedback endpoint at: {server_url}")
    
    try:
        # Test feedback endpoint
        response = requests.post(
            server_url,
            json={"event": "user_corrected_volume"},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Feedback endpoint working: {data}")
            return True
        else:
            print(f"❌ Feedback endpoint failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Start it with: python start_crest.py")
        return False
    except Exception as e:
        print(f"❌ Error testing feedback endpoint: {e}")
        return False

def test_complete_flow():
    """Test the complete flow: subtitle -> action -> feedback"""
    print("\n🎯 Testing Complete Adaptive Flow:")
    print("-" * 35)
    
    base_url = "http://localhost:5003"
    
    # Step 1: Send subtitle that should trigger volume reduction
    print("1. Sending loud event subtitle...")
    try:
        response = requests.post(
            f"{base_url}/data",
            json={"text": "[explosion]"},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('action') == 'LOWER_VOLUME':
                print(f"✅ AI Decision: {data.get('confidence')} -> {data.get('action')}")
            else:
                print(f"❌ Unexpected action: {data.get('action')}")
                return False
        else:
            print(f"❌ Subtitle processing failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error in subtitle processing: {e}")
        return False
    
    # Step 2: Simulate user feedback
    print("2. Simulating user correction feedback...")
    try:
        response = requests.post(
            f"{base_url}/feedback",
            json={"event": "user_corrected_volume"},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ User feedback recorded successfully")
        else:
            print(f"❌ Feedback recording failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error recording feedback: {e}")
        return False
    
    print("✅ Complete adaptive flow working!")
    return True

def test_metrics_integration():
    """Test that metrics are being sent properly"""
    print("\n📊 Testing Metrics Integration:")
    print("-" * 30)
    
    # Send multiple feedback events to test metrics
    feedback_url = "http://localhost:5003/feedback"
    
    print("Sending multiple feedback events to test metrics...")
    
    for i in range(3):
        try:
            response = requests.post(
                feedback_url,
                json={"event": "user_corrected_volume"},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Feedback event {i+1}/3 sent")
            else:
                print(f"❌ Feedback event {i+1}/3 failed")
                return False
                
        except Exception as e:
            print(f"❌ Error sending feedback event {i+1}: {e}")
            return False
        
        time.sleep(0.5)  # Small delay between requests
    
    print("✅ All feedback events sent successfully")
    print("📈 Check Datadog for 'crest.user_correction.count' metric")
    return True

if __name__ == "__main__":
    print("🔄 Adaptive Agent Feedback Loop Test Suite")
    print("=" * 50)
    
    # Run tests
    endpoint_test = test_feedback_endpoint()
    flow_test = test_complete_flow()
    metrics_test = test_metrics_integration()
    
    print("\n" + "=" * 50)
    if endpoint_test and flow_test and metrics_test:
        print("🎉 All feedback loop tests passed!")
        print("\n🏆 ADAPTIVE AGENT FEATURES:")
        print("✅ Detects user volume corrections")
        print("✅ Sends feedback to server")
        print("✅ Records custom metrics for evaluation")
        print("✅ Creates learning loop for continuous improvement")
        print("\n📋 Next steps:")
        print("1. Load Chrome extension")
        print("2. Test on YouTube - manually adjust volume after agent changes it")
        print("3. Check Datadog for 'crest.user_correction.count' metric")
        print("4. This demonstrates 'creative eval' and 'continuous improvement'!")
    else:
        print("❌ Some feedback loop tests failed. Check the server logs.")