# Implementation Plan - Risk-First Approach

## Phase 1: Build the Bridge - Establish Core Communication (HIGHEST RISK)

- [x] 1. Create minimal Flask server and Chrome extension communication
  - Create bare minimum Flask app with single `/data` endpoint that returns "Hello"
  - Enable CORS with flask-cors to allow localhost extension requests
  - Create basic Chrome extension with manifest.json and service worker
  - Implement simple fetch request from extension to http://localhost:5000/data
  - **CRITICAL CHECKPOINT**: Verify extension can successfully communicate with local server with no CORS errors
  - _Requirements: 1.2, 1.3, 2.1_

## Phase 2: Build the Backend - The "Brain"

- [x] 2. Implement full Flask server with observability suite
  - Configure ddtrace-run for automatic APM instrumentation
  - Set up structured JSON logging with DD_LOGS_INJECTION=true
  - Initialize Datadog statsd client for custom metrics
  - Enhance `/data` endpoint to accept subtitle text via POST
  - _Requirements: 2.1, 2.3, 3.1, 3.2, 3.3_

- [x] 3. Integrate AI gateway for subtitle processing
  - Configure OpenAI client to use TrueFoundry base_url and API key from environment variables
  - Create function to send subtitle text to OpenAI via TrueFoundry gateway
  - Implement simple YES/NO prompt for loud event detection (test with "[explosion]")
  - Add response validation and error handling
  - **CHECKPOINT**: Backend can process hardcoded subtitle text and send observability data to Datadog
  - _Requirements: 2.1, 2.2_

## Phase 3: Build the Frontend - The "Sensor" and "Actuator"

- [x] 4. Implement Chrome extension YouTube integration
  - Add proper permissions to manifest.json (scripting, webNavigation, YouTube host permissions)
  - Implement webNavigation listener in service worker to inject content script on YouTube video pages
  - Create content script with MutationObserver to watch .ytp-caption-segment elements
  - Implement volume control functions that can manipulate HTML5 video element
  - **CHECKPOINT**: Extension can read subtitles from live video and has volume control ready
  - _Requirements: 1.1, 1.4_

- [x] 5. Connect extension components for data flow
  - Set up chrome.runtime.sendMessage communication between content script and service worker
  - Implement HTTP POST requests from service worker to Flask server
  - Handle server responses and send volume adjustment commands back to content script
  - _Requirements: 1.2, 1.3_

## Phase 4: Final Integration and Testing

- [x] 6. Wire together end-to-end flow and comprehensive testing
  - Connect MutationObserver output to service worker's fetch calls
  - Connect server AI responses to content script's volume control functions
  - Test complete flow: subtitle detection → AI processing → volume adjustment
  - Verify observability data appears in Datadog (traces, logs, metrics)
  - Test with multiple subtitle examples ([explosion], [music], [gunshot], normal dialogue)
  - **FINAL CHECKPOINT**: Polished working demo with full observability
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 3.1, 3.2, 3.3_