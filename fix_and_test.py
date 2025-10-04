#!/usr/bin/env python3
"""
Fix and Test Script
Quickly diagnose and fix common issues, then run automated tests
"""

import requests
import subprocess
import sys
import os
import json
import time

def check_server():
    """Check if Flask server is running"""
    try:
        response = requests.get("http://localhost:5003/health", timeout=3)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

def test_ai_endpoint():
    """Test the AI endpoint with known cases"""
    test_cases = [
        ("[explosion]", "LOWER_VOLUME", "Should detect loud event"),
        ("Hello there", "NONE", "Should ignore quiet content")
    ]
    
    results = []
    
    for subtitle, expected_action, description in test_cases:
        try:
            response = requests.post(
                "http://localhost:5003/data",
                json={"text": subtitle},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_action = result.get("action", "NONE")
                is_correct = actual_action == expected_action
                
                results.append({
                    'subtitle': subtitle,
                    'expected': expected_action,
                    'actual': actual_action,
                    'correct': is_correct,
                    'description': description
                })
            else:
                results.append({
                    'subtitle': subtitle,
                    'error': f'HTTP {response.status_code}',
                    'description': description
                })
                
        except Exception as e:
            results.append({
                'subtitle': subtitle,
                'error': str(e),
                'description': description
            })
    
    return results

def check_extension_files():
    """Check if extension files exist and are properly configured"""
    required_files = [
        "chrome-extension/manifest.json",
        "chrome-extension/content-script-enhanced.js",
        "chrome-extension/service_worker.js",
        "chrome-extension/popup.html",
        "chrome-extension/popup.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    return missing_files

def check_environment():
    """Check environment variables and configuration"""
    env_vars = {
        'TRUEFOUNDRY_API_KEY': os.getenv('TRUEFOUNDRY_API_KEY'),
        'TRUEFOUNDRY_BASE_URL': os.getenv('TRUEFOUNDRY_BASE_URL'),
        'DD_SERVICE': os.getenv('DD_SERVICE'),
        'DD_ENV': os.getenv('DD_ENV')
    }
    
    return env_vars

def main():
    print("🔧 CREST FIX AND TEST UTILITY")
    print("=" * 50)
    
    # 1. Check server status
    print("1️⃣ Checking Flask server...")
    server_running, server_info = check_server()
    
    if server_running:
        print("   ✅ Server is running")
        if server_info:
            print(f"   📊 Service: {server_info.get('service', 'unknown')}")
            print(f"   📊 Version: {server_info.get('version', 'unknown')}")
    else:
        print("   ❌ Server not accessible")
        print(f"   🔍 Error: {server_info}")
        print("\n   💡 To fix:")
        print("      python app.py")
        print("      or")
        print("      ddtrace-run python app.py")
        return
    
    # 2. Test AI endpoint
    print("\n2️⃣ Testing AI endpoint...")
    ai_results = test_ai_endpoint()
    
    correct_count = sum(1 for r in ai_results if r.get('correct', False))
    total_count = len(ai_results)
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"   📊 AI Accuracy: {accuracy:.1f}% ({correct_count}/{total_count})")
    
    for result in ai_results:
        if 'error' in result:
            print(f"   ❌ {result['subtitle']}: ERROR - {result['error']}")
        elif result['correct']:
            print(f"   ✅ {result['subtitle']}: {result['actual']} (correct)")
        else:
            print(f"   ❌ {result['subtitle']}: {result['actual']} (expected {result['expected']})")
    
    # 3. Check extension files
    print("\n3️⃣ Checking extension files...")
    missing_files = check_extension_files()
    
    if not missing_files:
        print("   ✅ All extension files present")
    else:
        print("   ❌ Missing files:")
        for file in missing_files:
            print(f"      - {file}")
    
    # 4. Check environment
    print("\n4️⃣ Checking environment...")
    env_vars = check_environment()
    
    has_ai_config = bool(env_vars['TRUEFOUNDRY_API_KEY'] and env_vars['TRUEFOUNDRY_BASE_URL'])
    has_datadog_config = bool(env_vars['DD_SERVICE'])
    
    if has_ai_config:
        print("   ✅ AI configuration found (Live Mode)")
        print(f"      API Key: {env_vars['TRUEFOUNDRY_API_KEY'][:10]}...")
        print(f"      Base URL: {env_vars['TRUEFOUNDRY_BASE_URL']}")
    else:
        print("   ⚠️ No AI configuration (Mock Mode)")
        print("      Set TRUEFOUNDRY_API_KEY and TRUEFOUNDRY_BASE_URL for live AI")
    
    if has_datadog_config:
        print("   ✅ Datadog configuration found")
        print(f"      Service: {env_vars['DD_SERVICE']}")
        print(f"      Environment: {env_vars['DD_ENV']}")
    else:
        print("   ⚠️ No Datadog configuration")
        print("      Set DD_SERVICE and DD_ENV for observability")
    
    # 5. Overall assessment
    print("\n🎯 OVERALL ASSESSMENT")
    print("=" * 30)
    
    if accuracy >= 80:
        print("🎉 SYSTEM STATUS: EXCELLENT")
        print("   Your AI is working intelligently!")
    elif accuracy >= 60:
        print("✅ SYSTEM STATUS: GOOD")
        print("   Your AI is working reasonably well")
    else:
        print("❌ SYSTEM STATUS: NEEDS ATTENTION")
        print("   Your AI may not be working correctly")
    
    # 6. Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 20)
    
    if accuracy < 80:
        print("• Check your AI configuration (API keys)")
        print("• Verify server logs for errors")
        print("• Try restarting the server")
    
    if missing_files:
        print("• Restore missing extension files")
        print("• Reload the extension in Chrome")
    
    if not has_ai_config:
        print("• Add AI credentials to .env file for live mode")
    
    print("\n🧪 NEXT STEPS")
    print("-" * 15)
    print("1. Run automated tests:")
    print("   python automated_test_suite.py")
    print()
    print("2. Start real-time dashboard:")
    print("   python test_dashboard.py")
    print()
    print("3. Test in browser:")
    print("   - Load extension in Chrome")
    print("   - Go to YouTube video with subtitles")
    print("   - Run live_youtube_tester.js in console")
    print()
    print("4. Manual testing:")
    print("   python monitor_ai_decisions.py")

if __name__ == "__main__":
    main()