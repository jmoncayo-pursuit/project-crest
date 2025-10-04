#!/usr/bin/env python3
"""
Live System Diagnostic Tool
Tests the complete Crest system end-to-end
"""

import requests
import json
import time
import sys

def test_server_health():
    """Test if the Flask server is responding"""
    print("🔍 Testing server health...")
    try:
        response = requests.get('http://localhost:5003/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server healthy: {data['service']} v{data['version']}")
            return True
        else:
            print(f"❌ Server unhealthy: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_subtitle_endpoint():
    """Test the subtitle processing endpoint"""
    print("\n🔍 Testing subtitle endpoint...")
    
    test_cases = [
        {"text": "[explosion]", "expected": "LOWER_VOLUME"},
        {"text": "Hello world", "expected": "NONE"},
        {"text": "[gunshot] [dramatic music]", "expected": "LOWER_VOLUME"},
        {"text": "Just normal conversation", "expected": "NONE"}
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: '{case['text']}'")
        try:
            response = requests.post(
                'http://localhost:5003/data',
                json={"text": case['text']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                confidence = data.get('confidence', 'UNKNOWN')
                
                if action == case['expected']:
                    print(f"    ✅ Correct action: {action} (confidence: {confidence})")
                else:
                    print(f"    ❌ Wrong action: {action}, expected: {case['expected']}")
                    
                print(f"    📊 Response: {json.dumps(data, indent=2)}")
            else:
                print(f"    ❌ HTTP Error: {response.status_code}")
                print(f"    📄 Response: {response.text}")
                
        except Exception as e:
            print(f"    ❌ Request failed: {e}")

def test_audio_endpoint():
    """Test the audio analysis endpoint"""
    print("\n🔍 Testing audio analysis endpoint...")
    
    test_cases = [
        {
            "name": "Loud spike",
            "data": {"volume": 0.8, "baseline": 0.2, "spike": 0.6},
            "expected": "LOWER_VOLUME"
        },
        {
            "name": "Normal audio",
            "data": {"volume": 0.3, "baseline": 0.25, "spike": 0.05},
            "expected": "NONE"
        },
        {
            "name": "Medium spike",
            "data": {"volume": 0.7, "baseline": 0.3, "spike": 0.4},
            "expected": "LOWER_VOLUME"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {case['name']}")
        print(f"    📊 Audio data: {case['data']}")
        
        try:
            response = requests.post(
                'http://localhost:5003/audio-data',
                json=case['data'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                confidence = data.get('confidence', 'UNKNOWN')
                
                if action == case['expected']:
                    print(f"    ✅ Correct action: {action} (confidence: {confidence})")
                else:
                    print(f"    ❌ Wrong action: {action}, expected: {case['expected']}")
                    
                print(f"    📊 Response: {json.dumps(data, indent=2)}")
            else:
                print(f"    ❌ HTTP Error: {response.status_code}")
                print(f"    📄 Response: {response.text}")
                
        except Exception as e:
            print(f"    ❌ Request failed: {e}")

def test_feedback_endpoint():
    """Test the feedback endpoint"""
    print("\n🔍 Testing feedback endpoint...")
    
    try:
        response = requests.post(
            'http://localhost:5003/feedback',
            json={"event": "user_corrected_volume"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ Feedback recorded: {data}")
        else:
            print(f"    ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"    ❌ Request failed: {e}")

def simulate_extension_workflow():
    """Simulate the complete extension workflow"""
    print("\n🔍 Simulating complete extension workflow...")
    
    # Step 1: Extension detects audio spike
    print("\n  Step 1: Audio spike detected by extension")
    audio_data = {
        "type": "audio_analysis",
        "volume": 0.85,
        "baseline": 0.2,
        "spike": 0.65,
        "timestamp": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(
            'http://localhost:5003/audio-data',
            json=audio_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ Server response: {data.get('action', 'UNKNOWN')}")
            
            if data.get('action') == 'LOWER_VOLUME':
                print(f"    📊 Volume level: {data.get('level', 'unknown')}")
                print(f"    ⏱️  Duration: {data.get('duration', 'unknown')}ms")
                
                # Step 2: Simulate user correction (if they disagree)
                print("\n  Step 2: User corrects volume (simulated)")
                feedback_response = requests.post(
                    'http://localhost:5003/feedback',
                    json={"event": "user_corrected_volume"},
                    timeout=5
                )
                
                if feedback_response.status_code == 200:
                    print("    ✅ User feedback recorded")
                else:
                    print(f"    ❌ Feedback failed: {feedback_response.status_code}")
            
        else:
            print(f"    ❌ Server error: {response.status_code}")
            
    except Exception as e:
        print(f"    ❌ Workflow failed: {e}")

def check_extension_manifest():
    """Check if the extension manifest is properly configured"""
    print("\n🔍 Checking extension configuration...")
    
    try:
        with open('chrome-extension/manifest.json', 'r') as f:
            manifest = json.load(f)
            
        print("    📄 Manifest.json analysis:")
        
        # Check content scripts
        if 'content_scripts' in manifest:
            scripts = manifest['content_scripts'][0]['js']
            print(f"    ✅ Content scripts: {scripts}")
            
            # Check which script is being used
            if 'content-script-audio.js' in scripts:
                print("    ⚠️  Using audio script (advanced)")
            elif 'content-script-working.js' in scripts:
                print("    ℹ️  Using working script (basic)")
            else:
                print("    ❌ Unknown content script")
        else:
            print("    ❌ No content scripts defined")
            
        # Check permissions
        permissions = manifest.get('permissions', [])
        host_permissions = manifest.get('host_permissions', [])
        
        print(f"    📋 Permissions: {permissions}")
        print(f"    🌐 Host permissions: {host_permissions}")
        
        # Check if localhost is allowed
        localhost_allowed = any('localhost:5003' in perm for perm in host_permissions)
        if localhost_allowed:
            print("    ✅ Localhost:5003 access allowed")
        else:
            print("    ❌ Localhost:5003 access not configured")
            
    except Exception as e:
        print(f"    ❌ Manifest check failed: {e}")

def main():
    """Run all diagnostic tests"""
    print("🚀 Crest Live System Diagnostic")
    print("=" * 50)
    
    # Test server
    if not test_server_health():
        print("\n❌ Server is not running. Start it with: python app.py")
        sys.exit(1)
    
    # Test endpoints
    test_subtitle_endpoint()
    test_audio_endpoint()
    test_feedback_endpoint()
    
    # Test workflow
    simulate_extension_workflow()
    
    # Check extension config
    check_extension_manifest()
    
    print("\n" + "=" * 50)
    print("🏁 Diagnostic complete!")
    print("\n💡 Next steps:")
    print("   1. Load the extension in Chrome (chrome://extensions/)")
    print("   2. Enable Developer mode")
    print("   3. Click 'Load unpacked' and select chrome-extension/ folder")
    print("   4. Go to a YouTube video with subtitles")
    print("   5. Check browser console for 'Crest Audio Agent' messages")

if __name__ == "__main__":
    main()