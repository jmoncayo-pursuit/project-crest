#!/usr/bin/env python3
"""
Automated Crest AI Testing Suite
Runs continuous automated tests to verify AI behavior
"""

import requests
import json
import time
import threading
import random
from datetime import datetime
from collections import deque
import statistics

class AutomatedTestSuite:
    def __init__(self):
        self.server_url = "http://localhost:5003"
        self.results = deque(maxlen=100)  # Keep last 100 results
        self.is_running = False
        self.stats = {
            'total_tests': 0,
            'correct_predictions': 0,
            'loud_events_detected': 0,
            'quiet_events_ignored': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'response_times': []
        }
        
        # Test cases
        self.loud_test_cases = [
            "[explosion]", "[gunshot]", "[thunder]", "[crash]", "[bang]", "[boom]",
            "[screaming]", "[shouting]", "[dramatic music]", "[intense music]",
            "BOOM! The building exploded", "Gunfire erupted from the alley",
            "Thunder crashed overhead", "The car crashed into the wall",
            "Loud music blasted from the speakers", "She screamed at the top of her lungs",
            "[sound of explosion]", "[gunshots firing]", "[loud crash]",
            "The bomb went off with a deafening boom"
        ]
        
        self.quiet_test_cases = [
            "Hello, how are you today?", "The cat walked quietly across the room",
            "She whispered softly", "The gentle breeze rustled the leaves",
            "He smiled and nodded", "The library was completely silent",
            "They had a quiet dinner together", "The baby slept peacefully",
            "It was a beautiful morning", "The flowers bloomed in spring",
            "She read a book by the window", "The coffee was still warm",
            "He typed quietly on his laptop", "The sunset painted the sky orange",
            "They walked hand in hand", "The museum was nearly empty",
            "She hummed a gentle tune", "The garden was full of butterflies"
        ]
    
    def check_server_health(self):
        """Check if the server is running and responsive"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_single_subtitle(self, subtitle_text, expected_type):
        """Test a single subtitle and return result"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.server_url}/data",
                json={"text": subtitle_text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response_time': response_time
                }
            
            result = response.json()
            decision = "LOUD" if result.get("action") == "LOWER_VOLUME" else "QUIET"
            is_correct = decision == expected_type
            
            return {
                'subtitle': subtitle_text,
                'expected': expected_type,
                'actual': decision,
                'correct': is_correct,
                'response_time': response_time,
                'confidence': result.get('confidence', 'unknown'),
                'level': result.get('level'),
                'duration': result.get('duration'),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'response_time': time.time() - start_time
            }
    
    def run_batch_test(self, num_tests=20):
        """Run a batch of random tests"""
        print(f"🧪 Running batch test with {num_tests} cases...")
        
        batch_results = []
        
        for i in range(num_tests):
            # Randomly choose loud or quiet test case
            if random.choice([True, False]):
                subtitle = random.choice(self.loud_test_cases)
                expected = "LOUD"
            else:
                subtitle = random.choice(self.quiet_test_cases)
                expected = "QUIET"
            
            print(f"  Test {i+1}/{num_tests}: {expected} - '{subtitle[:40]}{'...' if len(subtitle) > 40 else ''}'")
            
            result = self.test_single_subtitle(subtitle, expected)
            
            if 'error' in result:
                print(f"    ❌ Error: {result['error']}")
                continue
            
            batch_results.append(result)
            self.results.append(result)
            self.update_stats(result)
            
            # Show result
            if result['correct']:
                print(f"    ✅ Correct: {result['actual']} ({result['response_time']:.2f}s)")
            else:
                print(f"    ❌ Wrong: {result['actual']} (expected {result['expected']}) ({result['response_time']:.2f}s)")
            
            # Small delay to avoid overwhelming server
            time.sleep(0.2)
        
        return batch_results
    
    def update_stats(self, result):
        """Update running statistics"""
        self.stats['total_tests'] += 1
        self.stats['response_times'].append(result['response_time'])
        
        if result['correct']:
            self.stats['correct_predictions'] += 1
        
        if result['expected'] == 'LOUD' and result['actual'] == 'LOUD':
            self.stats['loud_events_detected'] += 1
        elif result['expected'] == 'QUIET' and result['actual'] == 'QUIET':
            self.stats['quiet_events_ignored'] += 1
        elif result['expected'] == 'QUIET' and result['actual'] == 'LOUD':
            self.stats['false_positives'] += 1
        elif result['expected'] == 'LOUD' and result['actual'] == 'QUIET':
            self.stats['false_negatives'] += 1
        
        # Keep only last 100 response times
        if len(self.stats['response_times']) > 100:
            self.stats['response_times'] = self.stats['response_times'][-100:]
    
    def print_stats(self):
        """Print current statistics"""
        if self.stats['total_tests'] == 0:
            print("📊 No tests completed yet")
            return
        
        accuracy = (self.stats['correct_predictions'] / self.stats['total_tests']) * 100
        avg_response_time = statistics.mean(self.stats['response_times']) if self.stats['response_times'] else 0
        
        print("\n📊 CURRENT STATISTICS")
        print("=" * 40)
        print(f"Total Tests: {self.stats['total_tests']}")
        print(f"Accuracy: {accuracy:.1f}% ({self.stats['correct_predictions']}/{self.stats['total_tests']})")
        print(f"Loud Events Detected: {self.stats['loud_events_detected']}")
        print(f"Quiet Events Ignored: {self.stats['quiet_events_ignored']}")
        print(f"False Positives: {self.stats['false_positives']}")
        print(f"False Negatives: {self.stats['false_negatives']}")
        print(f"Avg Response Time: {avg_response_time:.2f}s")
        
        # Interpretation
        if accuracy >= 90:
            print("🎉 EXCELLENT: AI is working perfectly!")
        elif accuracy >= 80:
            print("✅ GOOD: AI is working well")
        elif accuracy >= 70:
            print("⚠️ FAIR: AI is working but could be better")
        else:
            print("❌ POOR: AI may have issues")
    
    def continuous_testing(self, interval=30, batch_size=10):
        """Run continuous testing at regular intervals"""
        print(f"🔄 Starting continuous testing (every {interval}s, {batch_size} tests per batch)")
        print("Press Ctrl+C to stop")
        
        self.is_running = True
        
        try:
            while self.is_running:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Running automated batch...")
                
                if not self.check_server_health():
                    print("❌ Server not responding, waiting...")
                    time.sleep(10)
                    continue
                
                self.run_batch_test(batch_size)
                self.print_stats()
                
                print(f"\n💤 Waiting {interval}s until next batch...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️ Stopping continuous testing...")
            self.is_running = False
    
    def stress_test(self, num_requests=100, concurrent=5):
        """Run stress test with concurrent requests"""
        print(f"⚡ Running stress test: {num_requests} requests with {concurrent} concurrent threads")
        
        results = []
        threads = []
        
        def worker():
            for _ in range(num_requests // concurrent):
                subtitle = random.choice(self.loud_test_cases + self.quiet_test_cases)
                expected = "LOUD" if subtitle in self.loud_test_cases else "QUIET"
                
                result = self.test_single_subtitle(subtitle, expected)
                if 'error' not in result:
                    results.append(result)
                    self.update_stats(result)
        
        # Start threads
        for _ in range(concurrent):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        print(f"✅ Stress test completed: {len(results)} successful requests")
        self.print_stats()
    
    def consistency_test(self, subtitle, num_tests=10):
        """Test the same subtitle multiple times for consistency"""
        print(f"🔄 Testing consistency: '{subtitle}' ({num_tests} times)")
        
        results = []
        for i in range(num_tests):
            expected = "LOUD" if any(keyword in subtitle.lower() for keyword in 
                                  ['explosion', 'gunshot', 'thunder', 'crash', 'bang', 'boom', 'scream']) else "QUIET"
            
            result = self.test_single_subtitle(subtitle, expected)
            if 'error' not in result:
                results.append(result['actual'])
                print(f"  Test {i+1}: {result['actual']}")
        
        if results:
            unique_results = set(results)
            consistency = (results.count(results[0]) / len(results)) * 100
            
            print(f"\nConsistency: {consistency:.1f}%")
            print(f"Unique results: {list(unique_results)}")
            
            if len(unique_results) == 1:
                print("✅ Perfect consistency")
            elif consistency >= 80:
                print("✅ Good consistency")
            else:
                print("❌ Poor consistency - may indicate random behavior")

def main():
    suite = AutomatedTestSuite()
    
    print("🤖 CREST AUTOMATED TESTING SUITE")
    print("=" * 50)
    
    # Check server
    if not suite.check_server_health():
        print("❌ Server not accessible at http://localhost:5003")
        print("Please start the Flask server first!")
        return
    
    print("✅ Server is accessible")
    print()
    
    while True:
        print("Available tests:")
        print("1. Quick Batch Test (20 random tests)")
        print("2. Continuous Testing (runs every 30s)")
        print("3. Stress Test (100 concurrent requests)")
        print("4. Consistency Test (same subtitle 10 times)")
        print("5. Custom Batch Size")
        print("6. View Current Stats")
        print("7. Exit")
        print()
        
        try:
            choice = input("Choose test (1-7): ").strip()
            
            if choice == "1":
                suite.run_batch_test(20)
                suite.print_stats()
                
            elif choice == "2":
                suite.continuous_testing()
                
            elif choice == "3":
                suite.stress_test()
                
            elif choice == "4":
                subtitle = input("Enter subtitle to test: ").strip()
                if subtitle:
                    suite.consistency_test(subtitle)
                
            elif choice == "5":
                try:
                    size = int(input("Enter batch size: "))
                    suite.run_batch_test(size)
                    suite.print_stats()
                except ValueError:
                    print("Invalid number")
                    
            elif choice == "6":
                suite.print_stats()
                
            elif choice == "7":
                break
                
            else:
                print("Please enter 1-7")
                
            print()
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()