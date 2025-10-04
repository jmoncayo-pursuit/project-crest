#!/usr/bin/env python3
"""
AI Behavior Verification Tool
Tests whether the Crest agent is making intelligent decisions or random ones.
"""

import requests
import json
import time
from typing import List, Dict, Tuple

# Test server endpoint
SERVER_URL = "http://localhost:5003/data"

def test_subtitle_analysis(subtitle_text: str) -> Dict:
    """Send subtitle text to server and get AI decision"""
    try:
        response = requests.post(
            SERVER_URL,
            json={"text": subtitle_text},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Server error: {response.status_code}")
            return {"error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return {"error": str(e)}

def run_intelligence_test() -> None:
    """
    Test the AI with known loud vs quiet subtitles to verify intelligent behavior.
    If it's truly intelligent, it should consistently identify loud events.
    """
    
    print("🧪 CREST AI INTELLIGENCE TEST")
    print("=" * 50)
    print("Testing whether the AI makes intelligent decisions or random ones...\n")
    
    # Test cases: (subtitle_text, expected_decision, description)
    test_cases = [
        # LOUD EVENTS (should trigger volume reduction)
        ("[explosion]", "YES", "Explosion sound effect"),
        ("[gunshot]", "YES", "Gunshot sound effect"), 
        ("[dramatic music]", "YES", "Dramatic music"),
        ("[thunder]", "YES", "Thunder sound"),
        ("[crash]", "YES", "Crash sound"),
        ("BOOM! The building exploded", "YES", "Explosion in dialogue"),
        ("Gunfire erupted from the alley", "YES", "Gunfire description"),
        ("[screaming]", "YES", "Screaming sound effect"),
        
        # QUIET EVENTS (should NOT trigger volume reduction)
        ("Hello, how are you today?", "NO", "Normal conversation"),
        ("The cat walked quietly across the room", "NO", "Quiet description"),
        ("She whispered softly", "NO", "Whisper description"),
        ("The gentle breeze rustled the leaves", "NO", "Peaceful nature"),
        ("He smiled and nodded", "NO", "Silent action"),
        ("The library was completely silent", "NO", "Silence description"),
        ("They had a quiet dinner together", "NO", "Quiet activity"),
        ("The baby slept peacefully", "NO", "Peaceful scene"),
    ]
    
    results = []
    correct_predictions = 0
    total_tests = len(test_cases)
    
    print(f"Running {total_tests} test cases...\n")
    
    for i, (subtitle, expected, description) in enumerate(test_cases, 1):
        print(f"Test {i}/{total_tests}: {description}")
        print(f"  Subtitle: '{subtitle}'")
        print(f"  Expected: {expected}")
        
        # Send to AI for analysis
        result = test_subtitle_analysis(subtitle)
        
        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            results.append({
                "test": description,
                "subtitle": subtitle,
                "expected": expected,
                "actual": "ERROR",
                "correct": False,
                "error": result["error"]
            })
            continue
        
        # Extract AI decision
        actual_decision = "YES" if result.get("action") == "LOWER_VOLUME" else "NO"
        is_correct = actual_decision == expected
        
        if is_correct:
            correct_predictions += 1
            print(f"  ✅ Actual: {actual_decision} (CORRECT)")
        else:
            print(f"  ❌ Actual: {actual_decision} (WRONG - expected {expected})")
        
        results.append({
            "test": description,
            "subtitle": subtitle,
            "expected": expected,
            "actual": actual_decision,
            "correct": is_correct,
            "response": result
        })
        
        print()
        time.sleep(0.5)  # Small delay to avoid overwhelming server
    
    # Calculate accuracy
    accuracy = (correct_predictions / total_tests) * 100
    
    print("=" * 50)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Wrong Predictions: {total_tests - correct_predictions}")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    
    # Interpret results
    if accuracy >= 90:
        print("🎉 EXCELLENT: AI is making highly intelligent decisions!")
        print("   The system is working correctly and distinguishing loud vs quiet events.")
    elif accuracy >= 70:
        print("✅ GOOD: AI is making mostly intelligent decisions.")
        print("   The system is working but may need some fine-tuning.")
    elif accuracy >= 50:
        print("⚠️  MEDIOCRE: AI is making some intelligent decisions.")
        print("   The system may be partially working but needs improvement.")
    else:
        print("❌ POOR: AI appears to be making random decisions.")
        print("   The system may not be working correctly or using mock mode.")
    
    print()
    
    # Show detailed breakdown
    print("📊 DETAILED BREAKDOWN:")
    print("-" * 30)
    
    loud_tests = [r for r in results if r["expected"] == "YES"]
    quiet_tests = [r for r in results if r["expected"] == "NO"]
    
    loud_correct = sum(1 for r in loud_tests if r["correct"])
    quiet_correct = sum(1 for r in quiet_tests if r["correct"])
    
    print(f"Loud Event Detection: {loud_correct}/{len(loud_tests)} ({loud_correct/len(loud_tests)*100:.1f}%)")
    print(f"Quiet Event Detection: {quiet_correct}/{len(quiet_tests)} ({quiet_correct/len(quiet_tests)*100:.1f}%)")
    
    # Show errors if any
    errors = [r for r in results if not r["correct"]]
    if errors:
        print(f"\n❌ INCORRECT PREDICTIONS ({len(errors)}):")
        for error in errors:
            print(f"  • {error['test']}: Expected {error['expected']}, got {error['actual']}")
    
    return results, accuracy

def run_consistency_test() -> None:
    """
    Test the same subtitle multiple times to check for consistency.
    Random behavior would give different results each time.
    """
    
    print("\n🔄 CONSISTENCY TEST")
    print("=" * 50)
    print("Testing the same subtitle multiple times to check for consistency...\n")
    
    test_subtitle = "[explosion]"
    num_tests = 5
    
    print(f"Testing subtitle: '{test_subtitle}' ({num_tests} times)")
    print()
    
    results = []
    
    for i in range(num_tests):
        print(f"  Test {i+1}/{num_tests}...", end=" ")
        result = test_subtitle_analysis(test_subtitle)
        
        if "error" in result:
            print(f"ERROR: {result['error']}")
            continue
        
        decision = "YES" if result.get("action") == "LOWER_VOLUME" else "NO"
        results.append(decision)
        print(f"Decision: {decision}")
        
        time.sleep(0.3)
    
    # Analyze consistency
    if not results:
        print("❌ No valid results obtained")
        return
    
    unique_decisions = set(results)
    consistency = (results.count(results[0]) / len(results)) * 100
    
    print(f"\nResults: {results}")
    print(f"Unique decisions: {list(unique_decisions)}")
    print(f"Consistency: {consistency:.1f}%")
    
    if len(unique_decisions) == 1:
        print("✅ PERFECT CONSISTENCY: AI gives the same decision every time")
        print("   This indicates intelligent, deterministic behavior")
    elif consistency >= 80:
        print("✅ GOOD CONSISTENCY: AI is mostly consistent")
        print("   Minor variations may be due to API latency or processing")
    else:
        print("❌ POOR CONSISTENCY: AI gives different decisions")
        print("   This may indicate random behavior or system issues")

def main():
    """Run all AI behavior tests"""
    
    print("🚀 CREST AI BEHAVIOR VERIFICATION")
    print("This tool will help you determine if the AI is working intelligently")
    print("or just making random volume adjustments.\n")
    
    # Check server connectivity
    print("🔍 Checking server connectivity...")
    try:
        response = requests.get("http://localhost:5003/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Flask server is running on port 5003")
        return
    
    print()
    
    # Run intelligence test
    results, accuracy = run_intelligence_test()
    
    # Run consistency test
    run_consistency_test()
    
    print("\n" + "=" * 50)
    print("🏁 FINAL VERDICT")
    print("=" * 50)
    
    if accuracy >= 80:
        print("🎉 Your AI agent is working INTELLIGENTLY!")
        print("   It's making smart decisions based on subtitle content.")
        print("   Any volume changes you see are likely legitimate AI responses.")
    elif accuracy >= 60:
        print("✅ Your AI agent is working REASONABLY well.")
        print("   It's making mostly intelligent decisions with some errors.")
    else:
        print("❌ Your AI agent may NOT be working intelligently.")
        print("   It appears to be making random or incorrect decisions.")
        print("   Check your API keys and server configuration.")
    
    print(f"\nFinal Accuracy Score: {accuracy:.1f}%")
    print("\nTo test live on YouTube:")
    print("1. Open a YouTube video with subtitles")
    print("2. Look for subtitles containing [explosion], [gunshot], etc.")
    print("3. The AI should lower volume ONLY for those events")
    print("4. Normal dialogue should NOT trigger volume changes")

if __name__ == "__main__":
    main()