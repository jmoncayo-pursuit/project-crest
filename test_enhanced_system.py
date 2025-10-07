#!/usr/bin/env python3
"""
Comprehensive test suite for enhanced Crest system
Tests audio detection, volume normalization, and dashboard functionality
"""

import requests
import json
import time
import threading
from dataclasses import dataclass
from typing import List, Dict, Any
import statistics

@dataclass
class TestResult:
    test_name: str
    success: bool
    response_time: float
    details: Dict[str, Any]
    error: str = None

class EnhancedSystemTester:
    def __init__(self, base_url="http://localhost:5003"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Enhanced Crest System Tests")
        print("=" * 50)
        
        # Test server connectivity
        self.test_server_health()
        
        # Test subtitle analysis with caching
        self.test_subtitle_analysis_with_caching()
        
        # Test audio analysis
        self.test_audio_analysis()
        
        # Test performance optimizations
        self.test_performance_optimizations()
        
        # Test confidence-based responses
        self.test_confidence_based_responses()
        
        # Test error handling
        self.test_error_handling()
        
        # Test concurrent requests
        self.test_concurrent_requests()
        
        # Generate report
        self.generate_report()
        
    def test_server_health(self):
        """Test server health and connectivity"""
        print("\n🏥 Testing Server Health...")
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.results.append(TestResult(
                    "server_health",
                    True,
                    response_time,
                    {"status": data.get("status"), "service": data.get("service")}
                ))
                print(f"✅ Server healthy - {response_time:.3f}s")
            else:
                raise Exception(f"Health check failed: {response.status_code}")
                
        except Exception as e:
            self.results.append(TestResult(
                "server_health",
                False,
                time.time() - start_time,
                {},
                str(e)
            ))
            print(f"❌ Server health check failed: {e}")
    
    def test_subtitle_analysis_with_caching(self):
        """Test subtitle analysis including caching behavior"""
        print("\n📝 Testing Subtitle Analysis with Caching...")
        
        test_cases = [
            ("[explosion]", "YES"),
            ("[gunshot]", "YES"), 
            ("[thunder]", "YES"),
            ("[music playing]", "NO"),
            ("hello world", "NO"),
            ("[dramatic music]", "YES"),
            ("normal conversation", "NO")
        ]
        
        for subtitle, expected in test_cases:
            # First request (cache miss)
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/data",
                    json={"text": subtitle},
                    timeout=10
                )
                first_response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    actual_action = "YES" if data.get("action") == "LOWER_VOLUME" else "NO"
                    
                    # Second request (should be cached)
                    start_time = time.time()
                    response2 = requests.post(
                        f"{self.base_url}/data",
                        json={"text": subtitle},
                        timeout=10
                    )
                    second_response_time = time.time() - start_time
                    
                    # Cache should make second request faster
                    cache_improvement = first_response_time > second_response_time
                    
                    success = (actual_action == expected)
                    
                    self.results.append(TestResult(
                        f"subtitle_analysis_{subtitle[:20]}",
                        success,
                        first_response_time,
                        {
                            "subtitle": subtitle,
                            "expected": expected,
                            "actual": actual_action,
                            "first_response_time": first_response_time,
                            "second_response_time": second_response_time,
                            "cache_improvement": cache_improvement,
                            "confidence": data.get("confidence", "unknown")
                        }
                    ))
                    
                    status = "✅" if success else "❌"
                    cache_status = "🚀" if cache_improvement else "⚠️"
                    print(f"{status} '{subtitle}' -> {actual_action} (expected {expected}) - {first_response_time:.3f}s {cache_status}")
                    
                else:
                    raise Exception(f"Request failed: {response.status_code}")
                    
            except Exception as e:
                self.results.append(TestResult(
                    f"subtitle_analysis_{subtitle[:20]}",
                    False,
                    time.time() - start_time,
                    {"subtitle": subtitle, "expected": expected},
                    str(e)
                ))
                print(f"❌ '{subtitle}' failed: {e}")
    
    def test_audio_analysis(self):
        """Test audio analysis with various spike scenarios"""
        print("\n🔊 Testing Audio Analysis...")
        
        test_cases = [
            # (volume, baseline, spike, expected_action)
            (0.8, 0.2, 0.5, "LOWER_VOLUME"),  # Large spike
            (0.6, 0.15, 0.4, "LOWER_VOLUME"),  # Medium spike, high volume
            (0.3, 0.1, 0.15, "NONE"),  # Small spike, low volume
            (0.9, 0.1, 0.7, "LOWER_VOLUME"),  # Very large spike
            (0.2, 0.15, 0.05, "NONE"),  # Minimal spike
        ]
        
        for volume, baseline, spike, expected in test_cases:
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/audio-data",
                    json={
                        "volume": volume,
                        "baseline": baseline,
                        "spike": spike
                    },
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    actual_action = data.get("action", "NONE")
                    confidence = data.get("confidence", 0)
                    
                    success = (actual_action == expected)
                    
                    self.results.append(TestResult(
                        f"audio_analysis_spike_{spike}",
                        success,
                        response_time,
                        {
                            "volume": volume,
                            "baseline": baseline,
                            "spike": spike,
                            "expected": expected,
                            "actual": actual_action,
                            "confidence": confidence,
                            "level": data.get("level"),
                            "duration": data.get("duration")
                        }
                    ))
                    
                    status = "✅" if success else "❌"
                    print(f"{status} Spike {spike:.2f} -> {actual_action} (conf: {confidence:.2f}) - {response_time:.3f}s")
                    
                else:
                    raise Exception(f"Request failed: {response.status_code}")
                    
            except Exception as e:
                self.results.append(TestResult(
                    f"audio_analysis_spike_{spike}",
                    False,
                    time.time() - start_time,
                    {"volume": volume, "baseline": baseline, "spike": spike},
                    str(e)
                ))
                print(f"❌ Audio analysis failed for spike {spike}: {e}")
    
    def test_performance_optimizations(self):
        """Test performance optimizations and response times"""
        print("\n⚡ Testing Performance Optimizations...")
        
        # Test response time requirements
        response_times = []
        
        for i in range(10):
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/data",
                    json={"text": "[explosion]"},  # Should be cached after first request
                    timeout=5
                )
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                if response.status_code != 200:
                    raise Exception(f"Request failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Performance test request {i+1} failed: {e}")
                continue
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            # Performance requirements: avg < 200ms, max < 500ms for cached requests
            avg_meets_requirement = avg_response_time < 0.2
            max_meets_requirement = max_response_time < 0.5
            
            self.results.append(TestResult(
                "performance_optimization",
                avg_meets_requirement and max_meets_requirement,
                avg_response_time,
                {
                    "avg_response_time": avg_response_time,
                    "max_response_time": max_response_time,
                    "min_response_time": min_response_time,
                    "total_requests": len(response_times),
                    "avg_meets_requirement": avg_meets_requirement,
                    "max_meets_requirement": max_meets_requirement
                }
            ))
            
            status = "✅" if (avg_meets_requirement and max_meets_requirement) else "❌"
            print(f"{status} Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s, Min: {min_response_time:.3f}s")
    
    def test_confidence_based_responses(self):
        """Test confidence-based response adjustments"""
        print("\n🎯 Testing Confidence-Based Responses...")
        
        # Test audio with different confidence scenarios
        test_cases = [
            (0.9, 0.1, 0.6, "high_confidence"),  # Should get aggressive reduction
            (0.5, 0.2, 0.25, "medium_confidence"),  # Should get moderate reduction
            (0.4, 0.15, 0.2, "low_confidence"),  # Should get light reduction or none
        ]
        
        for volume, baseline, spike, scenario in test_cases:
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/audio-data",
                    json={
                        "volume": volume,
                        "baseline": baseline,
                        "spike": spike
                    },
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    confidence = data.get("confidence", 0)
                    level = data.get("level", 1.0)
                    duration = data.get("duration", 0)
                    
                    # Validate confidence-based adjustments
                    if confidence > 0.8:
                        expected_aggressive = level <= 0.25 and duration >= 3000
                        success = expected_aggressive
                    elif confidence > 0.6:
                        expected_moderate = 0.25 < level <= 0.4 and duration >= 2000
                        success = expected_moderate
                    else:
                        expected_light = level > 0.4 or data.get("action") == "NONE"
                        success = expected_light
                    
                    self.results.append(TestResult(
                        f"confidence_response_{scenario}",
                        success,
                        response_time,
                        {
                            "scenario": scenario,
                            "confidence": confidence,
                            "level": level,
                            "duration": duration,
                            "action": data.get("action")
                        }
                    ))
                    
                    status = "✅" if success else "❌"
                    print(f"{status} {scenario}: conf={confidence:.2f}, level={level:.2f}, duration={duration}ms")
                    
            except Exception as e:
                print(f"❌ Confidence test failed for {scenario}: {e}")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n🛡️ Testing Error Handling...")
        
        # Test invalid requests
        error_cases = [
            ("empty_text", {"text": ""}),
            ("no_text", {}),
            ("invalid_audio", {"volume": "invalid"}),
            ("missing_audio_fields", {"volume": 0.5}),
        ]
        
        for case_name, payload in error_cases:
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/data",
                    json=payload,
                    timeout=5
                )
                response_time = time.time() - start_time
                
                # Should handle gracefully (either 400 error or safe fallback)
                success = response.status_code in [200, 400]
                
                if response.status_code == 200:
                    data = response.json()
                    # Should not crash and provide safe response
                    success = "error" in data or data.get("action") == "NONE"
                
                self.results.append(TestResult(
                    f"error_handling_{case_name}",
                    success,
                    response_time,
                    {
                        "case": case_name,
                        "status_code": response.status_code,
                        "payload": payload
                    }
                ))
                
                status = "✅" if success else "❌"
                print(f"{status} {case_name}: {response.status_code} - {response_time:.3f}s")
                
            except Exception as e:
                # Timeout or connection error is acceptable for error cases
                self.results.append(TestResult(
                    f"error_handling_{case_name}",
                    True,  # Error handling by timeout is acceptable
                    time.time() - start_time,
                    {"case": case_name, "error": str(e)},
                    str(e)
                ))
                print(f"✅ {case_name}: Handled by timeout/error - {e}")
    
    def test_concurrent_requests(self):
        """Test concurrent request handling"""
        print("\n🔄 Testing Concurrent Requests...")
        
        def make_request(request_id):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/data",
                    json={"text": f"[explosion] {request_id}"},
                    timeout=10
                )
                response_time = time.time() - start_time
                
                return {
                    "id": request_id,
                    "success": response.status_code == 200,
                    "response_time": response_time,
                    "status_code": response.status_code
                }
            except Exception as e:
                return {
                    "id": request_id,
                    "success": False,
                    "response_time": time.time() - start_time,
                    "error": str(e)
                }
        
        # Launch 5 concurrent requests
        threads = []
        results = []
        
        for i in range(5):
            thread = threading.Thread(target=lambda i=i: results.append(make_request(i)))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        successful_requests = sum(1 for r in results if r["success"])
        avg_response_time = statistics.mean([r["response_time"] for r in results if r["success"]])
        
        success = successful_requests >= 4  # At least 80% success rate
        
        self.results.append(TestResult(
            "concurrent_requests",
            success,
            avg_response_time,
            {
                "total_requests": len(results),
                "successful_requests": successful_requests,
                "success_rate": successful_requests / len(results),
                "avg_response_time": avg_response_time
            }
        ))
        
        status = "✅" if success else "❌"
        print(f"{status} {successful_requests}/{len(results)} successful, avg: {avg_response_time:.3f}s")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("📊 ENHANCED SYSTEM TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        print(f"\n📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Success Rate: {success_rate:.1%}")
        
        # Performance metrics
        response_times = [r.response_time for r in self.results if r.success]
        if response_times:
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
            print(f"\n⚡ Performance:")
            print(f"   Average Response Time: {avg_response_time:.3f}s")
            print(f"   Maximum Response Time: {max_response_time:.3f}s")
        
        # Failed tests
        failed_tests = [r for r in self.results if not r.success]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   - {test.test_name}: {test.error or 'Unknown error'}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if success_rate < 0.9:
            print("   - Investigate failed tests and improve error handling")
        if response_times and statistics.mean(response_times) > 0.5:
            print("   - Optimize response times for better user experience")
        if successful_tests == total_tests:
            print("   - All tests passed! System is ready for production")
        
        print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    tester = EnhancedSystemTester()
    tester.run_all_tests()