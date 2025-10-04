#!/usr/bin/env python3
"""
Live test to trigger your Chrome extension - simulates subtitle data
"""
import requests
import time

def trigger_agent():
    """Send test data to your agent to see it work"""
    print("🎬 Testing Your Crest Agent Live!")
    print("=" * 50)
    
    # Test cases that will trigger volume reduction
    loud_events = [
        "[explosion]",
        "[gunshot]", 
        "[dramatic music]",
        "[thunder]",
        "[car crash]"
    ]
    
    print("Sending loud events to your agent...")
    print("Watch your YouTube tab for volume changes and icon flashing!")
    print()
    
    for i, event in enumerate(loud_events, 1):
        try:
            print(f"🔊 Test {i}: Sending '{event}'...")
            
            response = requests.post(
                'http://localhost:5003/data',
                json={'text': event},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('action') == 'LOWER_VOLUME':
                    print(f"   ✅ Agent responded: LOWER VOLUME to {int(data.get('level', 0)*100)}%")
                    print(f"   🎯 Your Chrome extension should now:")
                    print(f"      - Flash the icon from gray to colored")
                    print(f"      - Lower YouTube volume for {data.get('duration', 0)}ms")
                    print(f"      - Show notification on screen")
                else:
                    print(f"   ❌ Unexpected response: {data}")
            else:
                print(f"   ❌ Server error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(3)  # Wait between tests
    
    print("🎉 Test complete! Did you see the volume changes and icon flashing?")

if __name__ == "__main__":
    trigger_agent()