#!/usr/bin/env python3
"""
Real-time Testing Dashboard
Shows live AI performance metrics and testing results
"""

import requests
import json
import time
import threading
import random
from datetime import datetime, timedelta
import os
import sys

class TestDashboard:
    def __init__(self):
        self.server_url = "http://localhost:5003"
        self.metrics = {
            'total_tests': 0,
            'correct': 0,
            'accuracy': 0.0,
            'avg_response_time': 0.0,
            'last_test_time': None,
            'server_status': 'Unknown',
            'recent_results': []
        }
        self.is_running = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def check_server(self):
        """Check server health"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=3)
            self.metrics['server_status'] = '🟢 Online' if response.status_code == 200 else '🟡 Issues'
            return response.status_code == 200
        except:
            self.metrics['server_status'] = '🔴 Offline'
            return False
    
    def run_single_test(self):
        """Run a single random test"""
        loud_cases = ["[explosion]", "[gunshot]", "[thunder]", "[crash]"]
        quiet_cases = ["Hello there", "The cat walked quietly", "She whispered softly", "It was peaceful"]
        
        if random.choice([True, False]):
            subtitle = random.choice(loud_cases)
            expected = "LOUD"
        else:
            subtitle = random.choice(quiet_cases)
            expected = "QUIET"
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.server_url}/data",
                json={"text": subtitle},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                actual = "LOUD" if result.get("action") == "LOWER_VOLUME" else "QUIET"
                is_correct = actual == expected
                
                # Update metrics
                self.metrics['total_tests'] += 1
                if is_correct:
                    self.metrics['correct'] += 1
                
                self.metrics['accuracy'] = (self.metrics['correct'] / self.metrics['total_tests']) * 100
                self.metrics['avg_response_time'] = response_time
                self.metrics['last_test_time'] = datetime.now()
                
                # Store recent result
                test_result = {
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'subtitle': subtitle[:30] + '...' if len(subtitle) > 30 else subtitle,
                    'expected': expected,
                    'actual': actual,
                    'correct': is_correct,
                    'response_time': response_time
                }
                
                self.metrics['recent_results'].append(test_result)
                if len(self.metrics['recent_results']) > 10:
                    self.metrics['recent_results'].pop(0)
                
                return test_result
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def display_dashboard(self):
        """Display the real-time dashboard"""
        self.clear_screen()
        
        print("🤖 CREST AI TESTING DASHBOARD")
        print("=" * 60)
        print(f"Server Status: {self.metrics['server_status']}")
        print(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Main metrics
        print("📊 PERFORMANCE METRICS")
        print("-" * 30)
        print(f"Total Tests: {self.metrics['total_tests']}")
        print(f"Accuracy: {self.metrics['accuracy']:.1f}% ({self.metrics['correct']}/{self.metrics['total_tests']})")
        print(f"Avg Response Time: {self.metrics['avg_response_time']:.2f}s")
        
        if self.metrics['last_test_time']:
            time_since = datetime.now() - self.metrics['last_test_time']
            print(f"Last Test: {time_since.seconds}s ago")
        
        # Accuracy indicator
        accuracy = self.metrics['accuracy']
        if accuracy >= 90:
            status = "🎉 EXCELLENT"
        elif accuracy >= 80:
            status = "✅ GOOD"
        elif accuracy >= 70:
            status = "⚠️ FAIR"
        else:
            status = "❌ POOR"
        
        print(f"AI Status: {status}")
        print()
        
        # Recent results
        print("📋 RECENT TEST RESULTS")
        print("-" * 30)
        
        if not self.metrics['recent_results']:
            print("No tests run yet...")
        else:
            print("Time     | Expected | Actual | Result | Response")
            print("-" * 50)
            
            for result in reversed(self.metrics['recent_results'][-5:]):  # Show last 5
                icon = "✅" if result['correct'] else "❌"
                print(f"{result['time']} | {result['expected']:8} | {result['actual']:6} | {icon:6} | {result['response_time']:.2f}s")
        
        print()
        print("🔄 Running automated tests... Press Ctrl+C to stop")
    
    def run_continuous_dashboard(self):
        """Run the dashboard with continuous testing"""
        self.is_running = True
        
        def test_worker():
            """Background thread that runs tests"""
            while self.is_running:
                if self.check_server():
                    self.run_single_test()
                time.sleep(2)  # Test every 2 seconds
        
        # Start background testing
        test_thread = threading.Thread(target=test_worker, daemon=True)
        test_thread.start()
        
        try:
            while self.is_running:
                self.display_dashboard()
                time.sleep(1)  # Update display every second
                
        except KeyboardInterrupt:
            self.is_running = False
            print("\n\n⏹️ Dashboard stopped")
            
            # Final summary
            print("\n📊 FINAL SUMMARY")
            print("=" * 30)
            print(f"Total Tests: {self.metrics['total_tests']}")
            print(f"Final Accuracy: {self.metrics['accuracy']:.1f}%")
            
            if self.metrics['accuracy'] >= 80:
                print("🎉 Your AI is working well!")
            elif self.metrics['accuracy'] >= 60:
                print("✅ Your AI is working reasonably")
            else:
                print("❌ Your AI may need attention")

def main():
    dashboard = TestDashboard()
    
    print("🚀 Starting Crest AI Testing Dashboard...")
    print("This will run continuous automated tests and show real-time results")
    print()
    
    # Initial server check
    if not dashboard.check_server():
        print("❌ Cannot connect to server at http://localhost:5003")
        print("Please make sure your Flask server is running!")
        print()
        print("Start it with:")
        print("  python app.py")
        print("  or")
        print("  ddtrace-run python app.py")
        return
    
    print("✅ Server is accessible")
    print("Starting dashboard in 3 seconds...")
    time.sleep(3)
    
    dashboard.run_continuous_dashboard()

if __name__ == "__main__":
    main()