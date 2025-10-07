#!/usr/bin/env python3
"""
Complete enhanced system validation test
Validates all components working together: audio detection, volume normalization, dashboard, and performance
"""

import subprocess
import sys
import time
import requests
import json

def check_server_running():
    """Check if the Flask server is running"""
    try:
        response = requests.get("http://localhost:5003/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_test_suite(test_name, script_name):
    """Run a test suite and return results"""
    print(f"\n{'='*60}")
    print(f"🧪 RUNNING: {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED")
            return True, result.stdout
        else:
            print(f"❌ {test_name} FAILED")
            print(f"Error output: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMED OUT")
        return False, "Test timed out after 5 minutes"
    except Exception as e:
        print(f"💥 {test_name} CRASHED: {e}")
        return False, str(e)

def main():
    """Run complete enhanced system validation"""
    print("🚀 COMPLETE ENHANCED SYSTEM VALIDATION")
    print("=" * 60)
    print("This test suite validates all enhanced Crest components:")
    print("- Real-time audio monitoring")
    print("- Enhanced volume control with smooth transitions")
    print("- Dual detection coordination (subtitle + audio)")
    print("- Performance optimizations and caching")
    print("- Enhanced dashboard functionality")
    print("- Comprehensive error handling")
    
    # Check if server is running
    print(f"\n🔍 Checking server status...")
    if not check_server_running():
        print("❌ Flask server is not running!")
        print("Please start the server with: ddtrace-run python app.py")
        print("Or: python app.py")
        return False
    
    print("✅ Flask server is running")
    
    # Test suites to run
    test_suites = [
        ("Enhanced System Tests", "test_enhanced_system.py"),
        ("Synthetic Audio Tests", "test_synthetic_audio.py"),
        ("Performance Benchmark", "test_performance_benchmark.py")
    ]
    
    results = {}
    overall_success = True
    
    # Run each test suite
    for test_name, script_name in test_suites:
        success, output = run_test_suite(test_name, script_name)
        results[test_name] = {"success": success, "output": output}
        
        if not success:
            overall_success = False
        
        # Small delay between test suites
        time.sleep(2)
    
    # Generate final report
    print(f"\n{'='*60}")
    print("📊 FINAL VALIDATION REPORT")
    print(f"{'='*60}")
    
    successful_tests = sum(1 for r in results.values() if r["success"])
    total_tests = len(results)
    success_rate = successful_tests / total_tests if total_tests > 0 else 0
    
    print(f"\n📈 Overall Results:")
    print(f"   Test Suites Run: {total_tests}")
    print(f"   Successful: {successful_tests}")
    print(f"   Success Rate: {success_rate:.1%}")
    
    print(f"\n📋 Test Suite Results:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    # System readiness assessment
    print(f"\n🎯 System Readiness Assessment:")
    
    if overall_success:
        print("   🎉 ALL TESTS PASSED!")
        print("   ✅ Enhanced Crest system is ready for production")
        print("   ✅ Real-time audio monitoring is functional")
        print("   ✅ Volume normalization is working correctly")
        print("   ✅ Dashboard provides real-time insights")
        print("   ✅ Performance meets requirements")
        
        print(f"\n🚀 Deployment Checklist:")
        print("   ✓ Load enhanced Chrome extension (manifest-enhanced.json)")
        print("   ✓ Use enhanced content script (content-script-enhanced-audio.js)")
        print("   ✓ Use enhanced service worker (service-worker-enhanced.js)")
        print("   ✓ Use enhanced popup (popup-enhanced.html)")
        print("   ✓ Start Flask server with: ddtrace-run python app.py")
        print("   ✓ Test on YouTube videos with dynamic audio")
        
    else:
        print("   ⚠️ SOME TESTS FAILED")
        print("   🔧 System needs attention before production deployment")
        
        failed_suites = [name for name, result in results.items() if not result["success"]]
        print(f"\n❌ Failed Test Suites:")
        for suite in failed_suites:
            print(f"   - {suite}")
        
        print(f"\n💡 Recommendations:")
        print("   1. Review failed test outputs above")
        print("   2. Fix identified issues")
        print("   3. Re-run validation suite")
        print("   4. Ensure all components are properly integrated")
    
    # Component status summary
    print(f"\n🔧 Enhanced Components Status:")
    print("   📁 Files Created:")
    print("      - chrome-extension/content-script-enhanced-audio.js")
    print("      - chrome-extension/service-worker-enhanced.js") 
    print("      - chrome-extension/popup-enhanced.html")
    print("      - chrome-extension/popup-enhanced.js")
    print("      - chrome-extension/manifest-enhanced.json")
    print("      - app.py (enhanced with caching and audio analysis)")
    print("      - test_enhanced_system.py")
    print("      - test_synthetic_audio.py")
    print("      - test_performance_benchmark.py")
    
    print(f"\n✨ Enhanced Features:")
    print("   🔊 Real-time audio level monitoring with Web Audio API")
    print("   🎛️ Smooth volume transitions with confidence-based adjustments")
    print("   📊 Enhanced dashboard with real-time activity logging")
    print("   🚀 Request caching and performance optimizations")
    print("   🔄 Dual detection coordination (subtitle + audio)")
    print("   🛡️ Improved error handling and resilience")
    print("   📈 Comprehensive testing and validation suite")
    
    print(f"\n🎊 Enhanced Crest System Validation Complete!")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)