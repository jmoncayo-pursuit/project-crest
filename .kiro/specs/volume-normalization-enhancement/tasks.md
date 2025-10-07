# Implementation Plan

- [x] 1. Implement real-time audio level monitoring in content script
  - Add Web Audio API integration to capture live audio levels from YouTube video element
  - Create AudioLevelMonitor class with baseline calculation and spike detection
  - Implement throttled audio analysis (10Hz) to prevent performance issues
  - Add audio context initialization with proper error handling for autoplay policies
  - _Requirements: 3.2, 4.3_

- [x] 2. Enhance volume controller with smooth transitions
  - Replace instant volume changes with gradual transitions over 500ms
  - Implement confidence-based partial volume reductions (50% for low confidence)
  - Add overlapping adjustment handling to prevent volume conflicts
  - Create VolumeController class to manage all volume operations centrally
  - _Requirements: 1.1, 1.3, 1.4_

- [x] 3. Add audio data processing endpoint to Flask server
  - Enhance existing /audio-data endpoint with improved AI analysis
  - Implement audio spike analysis using AI + heuristic hybrid approach
  - Add confidence calculation based on spike magnitude and AI decision
  - Create dynamic response levels based on audio analysis confidence
  - _Requirements: 3.2, 3.3_

- [x] 4. Implement request caching and performance optimizations
  - Add DecisionCache class for caching AI decisions (30s TTL)
  - Implement request deduplication to prevent simultaneous identical requests
  - Add fast local fallback when AI response exceeds 500ms timeout
  - Create baseline caching per video for improved accuracy
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 5. Enhance dashboard with real-time activity logging
  - Update service worker to send detailed event data to popup
  - Implement DashboardManager class for real-time statistics tracking
  - Add confidence level visualization and AI reasoning display
  - Create user correction tracking for accuracy metrics calculation
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 6. Integrate dual detection system (subtitle + audio)
  - Coordinate subtitle monitoring with audio level monitoring
  - Implement intelligent decision fusion when both systems detect events
  - Add prevention of duplicate volume adjustments from multiple triggers
  - Create unified event logging for both detection methods
  - _Requirements: 1.2, 3.2, 3.4_

- [x] 7. Add comprehensive testing and validation
  - Create synthetic audio test cases with known loud events
  - Test with various YouTube content types (action, gaming, music)
  - Validate smooth volume transitions and response timing
  - Measure and optimize CPU usage and response latency
  - _Requirements: 4.1, 4.4_