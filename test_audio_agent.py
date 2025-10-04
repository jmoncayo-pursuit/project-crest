#!/usr/bin/env python3
"""
Test the new audio-based Crest AI Agent
Tests real-time audio analysis instead of just subtitle processing
"""
import requests
import json
import time
from datetime import datetime

def test_audio_analysis():
    """Test the new audio analysis endpoint"""
    print("🎵 Testing Audio-Based AI Agent")
    print("=" * 50)
    
    # Test cases simulating different audio scenarios
    audio_test_cases = [
        {
            "volume": 0.9,
            "baseline": 0.3,
            "spike": 0.6,
            "description": "Explosion/Gunshot (Very Loud Spike)",
            "expected": "LOWER_VOLUME"
        },
        {
            "volume": 0.8,
            "baseline": 0.4,
            "spike": 0.4,
            "description": "Dramatic Music/Thunder (Loud Spike)",
            "expected": "LOWER_VOLUME"
        },
        {
            "volume": 0.7,
            "baseline": 0.5,
            "spike": 0.2,
            "description": "Normal Speech Volume Change",
            "expected": "NONE"
        },
        {
            "volume": 0.4,
            "baseline": 0.35,
            "spike": 0.05,
            "description": "Quiet Background Music",
            "expected": "NONE"
        },
        {
            "volume": 0.95,
            "baseline": 0.2,
            "spike": 0.75,
            "description": "Car Crash/Explosion (Massive Spike)",
            "expected": "LOWER_VOLUME"
        }
    ]
    
    print("Sending audio analysis data to server...\n")
    
    for i, test_case in enumerate(audio_test_cases, 1):
        try:
            # This is what the Chrome extension sends for audio events
            response = requests.post(
                'http://localhost:5003/audio-data',
                headers={'Content-Type': 'application/json'},
                json={
                    'type': 'audio_analysis',
                    'volume': test_case['volume'],
                    'baseline': test_case['baseline'],
                    'spike': test_case['spike'],
                    'timestamp': int(time.time() * 1000)
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                action = data.get('action', 'UNKNOWN')
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                if action == 'LOWER_VOLUME':
                    print(f"🔊 Test {i}: {test_case['description']}")
                    print(f"   📊 Volume: {test_case['volume']:.2f}, Baseline: {test_case['baseline']:.2f}, Spike: {test_case['spike']:.2f}")
                    print(f"   → 🔇 VOLUME LOWERED to {int(data.get('level', 0) * 100)}% for {data.get('duration', 0)}ms")
                    print(f"   → 🎯 Icon should flash ACTIVE")
                    
                    # Check if AI was used
                    if 'confidence' in data:
                        print(f"   → 🧠 AI Decision: {data['confidence']}")
                else:
                    print(f"💬 Test {i}: {test_case['description']}")
                    print(f"   📊 Volume: {test_case['volume']:.2f}, Baseline: {test_case['baseline']:.2f}, Spike: {test_case['spike']:.2f}")
                    print(f"   → ✅ Normal volume maintained")
                
                # Check if result matches expectation
                if action == test_case['expected']:
                    print(f"   ✅ Result matches expectation")
                else:
                    print(f"   ⚠️  Expected {test_case['expected']}, got {action}")
                    
            else:
                print(f"❌ Test {i}: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
        
        print()
        time.sleep(1)

def test_server_endpoints():
    """Test all server endpoints"""
    print("🔧 Testing Server Endpoints:")
    print("-" * 40)
    
    endpoints = [
        ('GET', '/health', None, 'Health check'),
        ('POST', '/data', {'text': '[explosion]'}, 'Subtitle processing'),
        ('POST', '/feedback', {'event': 'user_corrected_volume'}, 'User feedback'),
        ('POST', '/audio-data', {
            'type': 'audio_analysis',
            'volume': 0.8,
            'baseline': 0.3,
            'spike': 0.5,
            'timestamp': int(time.time() * 1000)
        }, 'Audio analysis')
    ]
    
    for method, endpoint, data, description in endpoints:
        try:
            url = f'http://localhost:5003{endpoint}'
            
            if method == 'GET':
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
            else:
                print(f"⚠️  {description}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: {e}")
    
    print()

def show_usage_guide():
    """Show how to use the new audio-based system"""
    print("🎯 HOW TO USE THE NEW AUDIO-BASED CREST AGENT:")
    print("=" * 60)
    print("1. 🔄 RELOAD CHROME EXTENSION:")
    print("   • Go to chrome://extensions/")
    print("   • Find 'Project Crest' extension")
    print("   • Click the reload button (↻)")
    print()
    print("2. 🎬 TEST WITH ANY VIDEO:")
    print("   • Open ANY YouTube video (captions not required!)")
    print("   • The agent now listens to actual audio")
    print("   • Look for videos with:")
    print("     - Action scenes (explosions, gunshots)")
    print("     - Gaming content (loud sound effects)")
    print("     - Music videos (dramatic volume changes)")
    print()
    print("3. 👀 WATCH FOR ACTIVITY:")
    print("   • Extension icon flashes when loud audio detected")
    print("   • Volume automatically lowers during loud moments")
    print("   • On-screen notification shows volume reduction")
    print()
    print("4. 🔧 DEBUG IN CHROME:")
    print("   • Press F12 → Console tab")
    print("   • Look for 'Crest Audio Agent:' messages")
    print("   • Watch for volume spike detections")
    print("   • Monitor API calls to localhost:5003/audio-data")
    print()
    print("5. 🧪 TEST WITH SIMULATION:")
    print("   • Open test_youtube_simulation.html")
    print("   • Use 'Simulate Loud Audio' buttons")
    print("   • Watch console for real-time audio analysis")
    print()

def main():
    print("🚀 CREST AUDIO-BASED AI AGENT TEST")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:5003/health', timeout=3)
        if response.status_code != 200:
            print("❌ Server not healthy!")
            return False
    except:
        print("❌ Server not running!")
        print("Start it with: python start_demo.py")
        return False
    
    print("✅ Server is running")
    print()
    
    # Test endpoints
    test_server_endpoints()
    
    # Test audio analysis
    test_audio_analysis()
    
    # Show usage guide
    show_usage_guide()
    
    print("🎉 AUDIO-BASED AGENT READY!")
    print("Your Crest agent now listens to real audio and detects loud events!")
    print("No more relying on subtitles - it works with ANY video! 🎵")

if __name__ == "__main__":
    main()