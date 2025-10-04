
This file contains the detailed technical specifications for the Chrome Extension component.

# SPECIFICATION: Chrome Extension

## 1\. File Structure

  - `manifest.json`
  - `service-worker.js`
  - `content-script.js`

## 2\. `manifest.json`

This file must be configured for Manifest V3. It requires permissions to interact with YouTube, inject scripts, and capture tab audio.

\*\*CODE:\*\*json
{
"manifest\_version": 3,
"name": "Project Crest",
"version": "1.0",
"description": "Intelligently manages browser media volume.",
"background": {
"service\_worker": "service-worker.js"
},
"permissions": [
"scripting",
"webNavigation",
"tabCapture"
],
"host\_permissions": [
"*://*[.youtube.com/](https://www.google.com/search?q=https://.youtube.com/)\*"
],
"action": {
"default\_title": "Crest"
}
}

```

## 3. `service-worker.js` (Event Coordinator)
- **Primary Role:** Detect navigation to a YouTube video page and inject the content script. This is necessary because YouTube is a Single-Page Application (SPA).[1, 2]
- **Implementation:**
  - Use the `chrome.webNavigation.onHistoryStateUpdated` event listener.
  - Filter for URLs that include `youtube.com/watch`.
  - On a match, use `chrome.scripting.executeScript()` to inject `content-script.js` into the active tab.[3, 4]
- **Communication:**
  - The service worker will receive messages from `content-script.js`.
  - It will forward this data to the local Flask server using `fetch()` to `http://localhost:5000/data`.

## 4. `content-script.js` (The Sensor & Actuator)
This script is injected directly into the YouTube page and performs two key functions.

### 4.1. Data Scraping (Sensor)
- **Subtitle Scraping:**
  - Use a `MutationObserver` to efficiently watch for changes in the DOM.[5, 6, 7]
  - The observer should target the element containing the caption/subtitle text (e.g., `.ytp-caption-segment`).
  - When a mutation occurs (i.e., new text appears), extract the `textContent` of the new node.
  - Send the extracted text to the `service-worker.js` using `chrome.runtime.sendMessage`.
- **Audio Level Analysis (Reactive Mode):**
  - The service worker must first get a `MediaStream` of the tab's audio using `chrome.tabCapture.capture()`.[8]
  - This stream is then processed using the Web Audio API.
  - Create an `AudioContext`, a `MediaStreamAudioSourceNode` from the stream, and an `AnalyserNode`.[9, 10]
  - In a `requestAnimationFrame` loop, use `analyser.getByteFrequencyData()` to get an array of frequency amplitudes.[10]
  - Calculate the Root Mean Square (RMS) of this array to get a single volume value, then convert it to Decibels Full Scale (dBFS).[11] This dBFS value is the real-time audio level.

### 4.2. Player Control (Actuator)
- **Mechanism:** The script will listen for messages from the service worker.
- **Action:** Upon receiving a "LOWER_VOLUME" command, it will directly manipulate the HTML5 `<video>` element.
- **Code:** Use `document.querySelector('video').volume = 0.5;` to set the volume. The target volume level will be part of the command payload.[12, 13] A `setTimeout` should be used to restore the volume after a specified duration.
```

-----
