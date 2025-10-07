#!/usr/bin/env python3
"""
Synthetic audio test generator for Crest system
Creates test scenarios with known loud events for validation
"""

import json
import time
import random
from typing import List, Tuple, Dict
import requests

class SyntheticAudioTester:
    def __init__(self, base_url="http://localhost:5003"):
        self.base_url = base_url
        
    def generate_audio_scenarios(self) -> List[Dict]:
        """Generate synthetic audio test scenarios"""
        scenarios = [
            # Explosion scenarios
            {
                "name": "Large Explosion",
                "volume": 0.85,
                "baseline": 0.15,
                "spike": 0.65,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.9,
                "description": "Sudden large explosion in action movie"
            },
            {
                "name": "Distant Explosion", 
                "volume": 0.45,
                "baseline": 0.12,
                "spike": 0.28,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.7,
                "description": "Distant explosion with moderate impact"
            },
            
            # Gunshot scenarios
            {
                "name": "Close Gunshot",
                "volume": 0.92,
                "baseline": 0.08,
                "spike": 0.78,
                "expected_action": "LOWER_VOLUME", 
                "expected_confidence": 0.95,
                "description": "Close-range gunshot in action scene"
            },
            {
                "name": "Multiple Gunshots",
                "volume": 0.75,
                "baseline": 0.20,
                "spike": 0.48,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.85,
                "description": "Rapid gunfire sequence"
            },
            
            # Music scenarios
            {
                "name": "Dramatic Music Swell",
                "volume": 0.80,
                "baseline": 0.25,
                "spike": 0.45,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.75,
                "description": "Orchestral crescendo in movie score"
            },
            {
                "name": "Bass Drop",
                "volume": 0.88,
                "baseline": 0.18,
                "spike": 0.58,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.8,
                "description": "Electronic music bass drop"
            },
            
            # Crash scenarios
            {
                "name": "Car Crash",
                "volume": 0.78,
                "baseline": 0.14,
                "spike": 0.52,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.85,
                "description": "Vehicle collision sound effect"
            },
            {
                "name": "Glass Breaking",
                "volume": 0.65,
                "baseline": 0.10,
                "spike": 0.42,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.75,
                "description": "Large glass window shattering"
            },
            
            # Thunder scenarios
            {
                "name": "Thunder Clap",
                "volume": 0.82,
                "baseline": 0.12,
                "spike": 0.62,
                "expected_action": "LOWER_VOLUME",
                "expected_confidence": 0.9,
                "description": "Close lightning thunder"
            },
            {
                "name": "Distant Thunder",
                "volume": 0.35,
                "baseline": 0.15,
                "spike": 0.18,
                "expected_action": "NONE",
                "expected_confidence": 0.6,
                "description": "Distant rumbling thunder"
            },
            
            # Normal scenarios (should NOT trigger)
            {
                "name": "Normal Dialogue",
                "volume": 0.35,
                "baseline": 0.30,
                "spike": 0.05,
                "expected_action": "NONE",
                "expected_confidence": 0.9,
                "description": "Regular conversation"
            },
            {
                "name": "Background Music",
                "volume": 0.25,
                "baseline": 0.22,
                "spike": 0.03,
                "expected_action": "NONE",
                "expected_confidence": 0.85,
                "description": "Soft background music"
            },
            {
                "name": "Ambient Noise",
                "volume": 0.18,
                "baseline": 0.16,
                "spike": 0.02,
                "expected_action": "NONE",
                "expected_confidence": 0.95,
                "description": "Environmental ambient sounds"
            },
            
            # Edge cases
            {
                "name": "Gradual Volume Increase",
                "volume": 0.70,
                "baseline": 0.40,
                "spike": 0.15,
                "expected_action": "NONE",
                "expected_confidence": 0.7,
                "description": "Slow volume increase (not sudden)"
            },
            {
                "name": "High Baseline Spike",
                "volume": 0.85,
                "baseline": 0.60,
                "spike": 0.20,
                "expected_action": "NONE",
                "expected_confidence": 0.6,
                "description": "Small spike on already loud baseline"
            }
        ]
        
        return scenarios
    
    def test_scenario(self, scenario: Dict) -> Dict:
        """Test a single audio scenario"""
        print(f"\n🎬 Testing: {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Audio Data: vol={scenario['volume']:.2f}, baseline={scenario['baseline']:.2f}, spike={scenario['spike']:.2f}")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/audio-data",
                json={
                    "volume": scenario["volume"],
                    "baseline": scenario["baseline"], 
                    "spike": scenario["spike"]
                },
                timeout=10
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                actual_action = data.get("action", "NONE")
                actual_confidence = data.get("confidence", 0)
                
                # Check if action matches expectation
                action_correct = actual_action == scenario["expected_action"]
                
                # Check if confidence is reasonable (within 0.2 of expected)
                confidence_reasonable = abs(actual_confidence - scenario["expected_confidence"]) <= 0.2
                
                success = action_correct and confidence_reasonable
                
                result = {
                    "scenario": scenario["name"],
                    "success": success,
                    "response_time": response_time,
                    "expected_action": scenario["expected_action"],
                    "actual_action": actual_action,
                    "expected_confidence": scenario["expected_confidence"],
                    "actual_confidence": actual_confidence,
                    "action_correct": action_correct,
                    "confidence_reasonable": confidence_reasonable,
                    "level": data.get("level"),
                    "duration": data.get("duration"),
                    "audio_data": {
                        "volume": scenario["volume"],
                        "baseline": scenario["baseline"],
                        "spike": scenario["spike"]
                    }
                }
                
                status = "✅" if success else "❌"
                action_status = "✓" if action_correct else "✗"
                conf_status = "✓" if confidence_reasonable else "✗"
                
                print(f"   {status} Action: {actual_action} {action_status} | Confidence: {actual_confidence:.2f} {conf_status} | Time: {response_time:.3f}s")
                
                if actual_action == "LOWER_VOLUME":
                    print(f"      → Level: {data.get('level', 'N/A')}, Duration: {data.get('duration', 'N/A')}ms")
                
                return result
                
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            result = {
                "scenario": scenario["name"],
                "success": False,
                "response_time": time.time() - start_time,
                "error": str(e),
                "audio_data": {
                    "volume": scenario["volume"],
                    "baseline": scenario["baseline"],
                    "spike": scenario["spike"]
                }
            }
            
            print(f"   ❌ Error: {e}")
            return result
    
    def run_all_scenarios(self):
        """Run all synthetic audio test scenarios"""
        print("🎵 SYNTHETIC AUDIO TEST SUITE")
        print("=" * 50)
        print("Testing AI audio detection with known synthetic scenarios")
        
        scenarios = self.generate_audio_scenarios()
        results = []
        
        for scenario in scenarios:
            result = self.test_scenario(scenario)
            results.append(result)
            
            # Small delay between tests
            time.sleep(0.5)
        
        self.generate_report(results)
        return results
    
    def generate_report(self, results: List[Dict]):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("📊 SYNTHETIC AUDIO TEST REPORT")
        print("=" * 50)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get("success", False))
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        # Categorize results
        loud_event_tests = [r for r in results if r.get("expected_action") == "LOWER_VOLUME"]
        normal_tests = [r for r in results if r.get("expected_action") == "NONE"]
        
        loud_event_success = sum(1 for r in loud_event_tests if r.get("action_correct", False))
        normal_success = sum(1 for r in normal_tests if r.get("action_correct", False))
        
        print(f"\n📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests}")
        print(f"   Success Rate: {success_rate:.1%}")
        
        print(f"\n🔊 Loud Event Detection:")
        print(f"   Tests: {len(loud_event_tests)}")
        print(f"   Correct: {loud_event_success}")
        print(f"   Accuracy: {loud_event_success/len(loud_event_tests):.1%}" if loud_event_tests else "   Accuracy: N/A")
        
        print(f"\n🔇 Normal Audio Detection:")
        print(f"   Tests: {len(normal_tests)}")
        print(f"   Correct: {normal_success}")
        print(f"   Accuracy: {normal_success/len(normal_tests):.1%}" if normal_tests else "   Accuracy: N/A")
        
        # Performance metrics
        successful_results = [r for r in results if r.get("success", False)]
        if successful_results:
            response_times = [r["response_time"] for r in successful_results]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            print(f"\n⚡ Performance:")
            print(f"   Average Response Time: {avg_response_time:.3f}s")
            print(f"   Maximum Response Time: {max_response_time:.3f}s")
        
        # Failed tests details
        failed_tests = [r for r in results if not r.get("success", False)]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                reason = []
                if not test.get("action_correct", True):
                    reason.append(f"action: got {test.get('actual_action')} expected {test.get('expected_action')}")
                if not test.get("confidence_reasonable", True):
                    reason.append(f"confidence: got {test.get('actual_confidence', 0):.2f} expected ~{test.get('expected_confidence', 0):.2f}")
                if test.get("error"):
                    reason.append(f"error: {test['error']}")
                
                print(f"   - {test['scenario']}: {', '.join(reason)}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        
        loud_accuracy = loud_event_success/len(loud_event_tests) if loud_event_tests else 1
        normal_accuracy = normal_success/len(normal_tests) if normal_tests else 1
        
        if loud_accuracy < 0.9:
            print("   - Improve loud event detection sensitivity")
        if normal_accuracy < 0.9:
            print("   - Reduce false positives for normal audio")
        if successful_results and avg_response_time > 0.5:
            print("   - Optimize AI processing for faster response times")
        if success_rate >= 0.95:
            print("   - Excellent performance! System ready for production")
        elif success_rate >= 0.85:
            print("   - Good performance with room for minor improvements")
        else:
            print("   - Significant improvements needed before production")
        
        print("\n🎉 Synthetic audio test suite completed!")

if __name__ == "__main__":
    tester = SyntheticAudioTester()
    tester.run_all_scenarios()