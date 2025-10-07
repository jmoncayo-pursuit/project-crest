#!/usr/bin/env python3
"""
Performance benchmark test for Crest system
Measures response times, CPU usage, and system limits
"""

import requests
import time
import threading
import statistics
import psutil
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

class PerformanceBenchmark:
    def __init__(self, base_url="http://localhost:5003"):
        self.base_url = base_url
        self.results = []
        
    def measure_response_times(self, num_requests=50):
        """Measure response times under normal load"""
        print(f"\n⏱️ Measuring Response Times ({num_requests} requests)...")
        
        response_times = []
        test_payloads = [
            {"text": "[explosion]"},
            {"text": "[gunshot]"},
            {"text": "normal dialogue"},
            {"text": "[thunder]"},
            {"text": "background music"}
        ]
        
        for i in range(num_requests):
            payload = test_payloads[i % len(test_payloads)]
            
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/data",
                    json=payload,
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    
                    if i % 10 == 0:
                        print(f"   Progress: {i+1}/{num_requests} - Latest: {response_time:.3f}s")
                        
            except Exception as e:
                print(f"   Request {i+1} failed: {e}")
        
        if response_times:
            avg_time = statistics.mean(response_times)
            median_time = statistics.median(response_times)
            p95_time = sorted(response_times)[int(0.95 * len(response_times))]
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n📊 Response Time Statistics:")
            print(f"   Average: {avg_time:.3f}s")
            print(f"   Median: {median_time:.3f}s")
            print(f"   95th Percentile: {p95_time:.3f}s")
            print(f"   Maximum: {max_time:.3f}s")
            print(f"   Minimum: {min_time:.3f}s")
            
            # Performance requirements check
            avg_meets_req = avg_time < 0.5  # 500ms average
            p95_meets_req = p95_time < 1.0  # 1s for 95th percentile
            
            print(f"\n✅ Performance Requirements:")
            print(f"   Average < 500ms: {'✓' if avg_meets_req else '✗'} ({avg_time:.3f}s)")
            print(f"   95th percentile < 1s: {'✓' if p95_meets_req else '✗'} ({p95_time:.3f}s)")
            
            return {
                "avg_time": avg_time,
                "median_time": median_time,
                "p95_time": p95_time,
                "max_time": max_time,
                "min_time": min_time,
                "total_requests": len(response_times),
                "avg_meets_req": avg_meets_req,
                "p95_meets_req": p95_meets_req
            }
        
        return None
    
    def test_concurrent_load(self, concurrent_users=10, requests_per_user=5):
        """Test system under concurrent load"""
        print(f"\n🔄 Testing Concurrent Load ({concurrent_users} users, {requests_per_user} requests each)...")
        
        def user_session(user_id):
            """Simulate a user session with multiple requests"""
            session_results = []
            
            for req_num in range(requests_per_user):
                start_time = time.time()
                try:
                    response = requests.post(
                        f"{self.base_url}/data",
                        json={"text": f"[explosion] user_{user_id}_req_{req_num}"},
                        timeout=15
                    )
                    response_time = time.time() - start_time
                    
                    session_results.append({
                        "user_id": user_id,
                        "request_num": req_num,
                        "success": response.status_code == 200,
                        "response_time": response_time,
                        "status_code": response.status_code
                    })
                    
                    # Small delay between requests from same user
                    time.sleep(0.1)
                    
                except Exception as e:
                    session_results.append({
                        "user_id": user_id,
                        "request_num": req_num,
                        "success": False,
                        "response_time": time.time() - start_time,
                        "error": str(e)
                    })
            
            return session_results
        
        # Execute concurrent user sessions
        all_results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_session, user_id) for user_id in range(concurrent_users)]
            
            for future in as_completed(futures):
                try:
                    session_results = future.result()
                    all_results.extend(session_results)
                except Exception as e:
                    print(f"   User session failed: {e}")
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = [r for r in all_results if r["success"]]
        failed_requests = [r for r in all_results if not r["success"]]
        
        success_rate = len(successful_requests) / len(all_results) if all_results else 0
        
        if successful_requests:
            response_times = [r["response_time"] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            max_response_time = max(response_times)
            
            # Calculate throughput
            throughput = len(successful_requests) / total_time
            
            print(f"\n📊 Concurrent Load Results:")
            print(f"   Total Requests: {len(all_results)}")
            print(f"   Successful: {len(successful_requests)}")
            print(f"   Failed: {len(failed_requests)}")
            print(f"   Success Rate: {success_rate:.1%}")
            print(f"   Average Response Time: {avg_response_time:.3f}s")
            print(f"   Max Response Time: {max_response_time:.3f}s")
            print(f"   Throughput: {throughput:.1f} requests/second")
            print(f"   Total Test Duration: {total_time:.1f}s")
            
            # Performance thresholds
            success_meets_req = success_rate >= 0.95
            response_meets_req = avg_response_time < 2.0  # More lenient under load
            throughput_meets_req = throughput >= 5.0  # At least 5 req/s
            
            print(f"\n✅ Load Test Requirements:")
            print(f"   Success Rate ≥ 95%: {'✓' if success_meets_req else '✗'} ({success_rate:.1%})")
            print(f"   Avg Response < 2s: {'✓' if response_meets_req else '✗'} ({avg_response_time:.3f}s)")
            print(f"   Throughput ≥ 5 req/s: {'✓' if throughput_meets_req else '✗'} ({throughput:.1f} req/s)")
            
            return {
                "total_requests": len(all_results),
                "successful_requests": len(successful_requests),
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "throughput": throughput,
                "total_duration": total_time,
                "success_meets_req": success_meets_req,
                "response_meets_req": response_meets_req,
                "throughput_meets_req": throughput_meets_req
            }
        
        return None
    
    def test_cache_performance(self):
        """Test caching system performance"""
        print(f"\n🚀 Testing Cache Performance...")
        
        # Test same request multiple times to measure cache effectiveness
        test_text = "[explosion] cache test"
        
        # First request (cache miss)
        print("   Testing cache miss...")
        start_time = time.time()
        response1 = requests.post(f"{self.base_url}/data", json={"text": test_text}, timeout=10)
        first_response_time = time.time() - start_time
        
        # Subsequent requests (should be cached)
        print("   Testing cache hits...")
        cache_response_times = []
        
        for i in range(5):
            start_time = time.time()
            response = requests.post(f"{self.base_url}/data", json={"text": test_text}, timeout=10)
            response_time = time.time() - start_time
            cache_response_times.append(response_time)
        
        if cache_response_times:
            avg_cache_time = statistics.mean(cache_response_times)
            cache_improvement = first_response_time / avg_cache_time if avg_cache_time > 0 else 1
            
            print(f"\n📊 Cache Performance:")
            print(f"   First Request (miss): {first_response_time:.3f}s")
            print(f"   Cached Requests (avg): {avg_cache_time:.3f}s")
            print(f"   Cache Improvement: {cache_improvement:.1f}x faster")
            
            # Cache should provide at least 2x improvement
            cache_effective = cache_improvement >= 2.0
            
            print(f"\n✅ Cache Requirements:")
            print(f"   Cache ≥ 2x faster: {'✓' if cache_effective else '✗'} ({cache_improvement:.1f}x)")
            
            return {
                "first_response_time": first_response_time,
                "avg_cache_time": avg_cache_time,
                "cache_improvement": cache_improvement,
                "cache_effective": cache_effective
            }
        
        return None
    
    def test_memory_usage(self):
        """Test memory usage during operation"""
        print(f"\n💾 Testing Memory Usage...")
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"   Initial Memory: {initial_memory:.1f} MB")
        
        # Make many requests to test for memory leaks
        print("   Making 100 requests to test memory stability...")
        
        memory_samples = [initial_memory]
        
        for i in range(100):
            try:
                requests.post(
                    f"{self.base_url}/data",
                    json={"text": f"[explosion] memory test {i}"},
                    timeout=5
                )
                
                if i % 20 == 0:
                    current_memory = process.memory_info().rss / 1024 / 1024
                    memory_samples.append(current_memory)
                    print(f"   Request {i}: {current_memory:.1f} MB")
                    
            except Exception as e:
                print(f"   Request {i} failed: {e}")
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        memory_increase_percent = (memory_increase / initial_memory) * 100
        
        print(f"\n📊 Memory Usage Results:")
        print(f"   Initial Memory: {initial_memory:.1f} MB")
        print(f"   Final Memory: {final_memory:.1f} MB")
        print(f"   Memory Increase: {memory_increase:.1f} MB ({memory_increase_percent:.1f}%)")
        
        # Memory increase should be reasonable (< 50% increase)
        memory_stable = memory_increase_percent < 50
        
        print(f"\n✅ Memory Requirements:")
        print(f"   Memory increase < 50%: {'✓' if memory_stable else '✗'} ({memory_increase_percent:.1f}%)")
        
        return {
            "initial_memory": initial_memory,
            "final_memory": final_memory,
            "memory_increase": memory_increase,
            "memory_increase_percent": memory_increase_percent,
            "memory_stable": memory_stable,
            "memory_samples": memory_samples
        }
    
    def run_full_benchmark(self):
        """Run complete performance benchmark suite"""
        print("🏁 PERFORMANCE BENCHMARK SUITE")
        print("=" * 50)
        
        results = {}
        
        # Response time test
        results["response_times"] = self.measure_response_times(50)
        
        # Concurrent load test
        results["concurrent_load"] = self.test_concurrent_load(10, 5)
        
        # Cache performance test
        results["cache_performance"] = self.test_cache_performance()
        
        # Memory usage test
        results["memory_usage"] = self.test_memory_usage()
        
        # Generate final report
        self.generate_benchmark_report(results)
        
        return results
    
    def generate_benchmark_report(self, results: Dict):
        """Generate comprehensive benchmark report"""
        print("\n" + "=" * 50)
        print("🏆 PERFORMANCE BENCHMARK REPORT")
        print("=" * 50)
        
        # Overall performance score
        score_components = []
        
        if results.get("response_times"):
            rt = results["response_times"]
            if rt["avg_meets_req"] and rt["p95_meets_req"]:
                score_components.append(25)  # Response time: 25 points
            elif rt["avg_meets_req"] or rt["p95_meets_req"]:
                score_components.append(15)
            else:
                score_components.append(5)
        
        if results.get("concurrent_load"):
            cl = results["concurrent_load"]
            load_score = 0
            if cl["success_meets_req"]: load_score += 10
            if cl["response_meets_req"]: load_score += 10
            if cl["throughput_meets_req"]: load_score += 5
            score_components.append(load_score)  # Load test: 25 points
        
        if results.get("cache_performance"):
            cp = results["cache_performance"]
            if cp["cache_effective"]:
                score_components.append(25)  # Cache: 25 points
            else:
                score_components.append(10)
        
        if results.get("memory_usage"):
            mu = results["memory_usage"]
            if mu["memory_stable"]:
                score_components.append(25)  # Memory: 25 points
            else:
                score_components.append(10)
        
        total_score = sum(score_components)
        max_score = 100
        
        print(f"\n🎯 Performance Score: {total_score}/{max_score} ({total_score/max_score:.1%})")
        
        # Grade the performance
        if total_score >= 90:
            grade = "A+ (Excellent)"
        elif total_score >= 80:
            grade = "A (Very Good)"
        elif total_score >= 70:
            grade = "B (Good)"
        elif total_score >= 60:
            grade = "C (Acceptable)"
        else:
            grade = "D (Needs Improvement)"
        
        print(f"📊 Performance Grade: {grade}")
        
        # Detailed breakdown
        print(f"\n📋 Score Breakdown:")
        if results.get("response_times"):
            rt_score = score_components[0] if score_components else 0
            print(f"   Response Times: {rt_score}/25")
        
        if results.get("concurrent_load"):
            cl_score = score_components[1] if len(score_components) > 1 else 0
            print(f"   Concurrent Load: {cl_score}/25")
        
        if results.get("cache_performance"):
            cp_score = score_components[2] if len(score_components) > 2 else 0
            print(f"   Cache Performance: {cp_score}/25")
        
        if results.get("memory_usage"):
            mu_score = score_components[3] if len(score_components) > 3 else 0
            print(f"   Memory Stability: {mu_score}/25")
        
        # Recommendations
        print(f"\n💡 Performance Recommendations:")
        
        if total_score >= 90:
            print("   🎉 Excellent performance! System is production-ready.")
        elif total_score >= 70:
            print("   ✅ Good performance with minor optimization opportunities.")
        else:
            print("   ⚠️ Performance improvements needed before production deployment.")
        
        if results.get("response_times") and not results["response_times"]["avg_meets_req"]:
            print("   - Optimize AI processing to reduce average response time")
        
        if results.get("concurrent_load") and not results["concurrent_load"]["success_meets_req"]:
            print("   - Improve error handling and system stability under load")
        
        if results.get("cache_performance") and not results["cache_performance"]["cache_effective"]:
            print("   - Optimize caching mechanism for better performance gains")
        
        if results.get("memory_usage") and not results["memory_usage"]["memory_stable"]:
            print("   - Investigate and fix potential memory leaks")
        
        print("\n🏁 Performance benchmark completed!")

if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    benchmark.run_full_benchmark()