# Project Crest - Final Integration Guide

## Prerequisites Setup

### 1. Environment Variables
Create a `.env` file or set these environment variables:

```bash
# TrueFoundry AI Gateway (Required)
export TRUEFOUNDRY_API_KEY="tfy-your-api-key-here"
export TRUEFOUNDRY_BASE_URL="https://your-truefoundry-endpoint"

# Datadog Observability (Required)
export DD_AGENT_HOST="localhost"
export DD_LOGS_INJECTION="true"
export DD_SERVICE="crest-agent"
export DD_ENV="development"
export DD_VERSION="0.1.0"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Datadog Agent
Ensure Datadog agent is running locally on port 8125 for StatsD metrics.

## Full Stack Integration

### Step 1: Start the Flask Server with Datadog Tracing
```bash
ddtrace-run python app.py
```

Expected output:
- Server starts on http://localhost:5000
- Datadog tracing enabled
- JSON structured logging active

### Step 2: Load Chrome Extension
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension/` directory
5. Verify extension appears with name "Project Crest"

### Step 3: End-to-End Testing

#### Test Video Recommendations:
- **Action Movie Trailers**: Search "action movie trailer" - lots of explosions
- **Gaming Content**: Search "FPS gameplay" - gunshots and explosions
- **Movie Clips**: Search "movie explosion scenes" - dramatic sound effects

#### Testing Procedure:
1. **Navigate to YouTube**: Go to any YouTube video with closed captions
2. **Enable Captions**: Click the CC button to turn on closed captions
3. **Find Loud Events**: Look for captions like:
   - `[explosion]`
   - `[gunshot]` 
   - `[dramatic music]`
   - `[thunder]`
   - `[crash]`
   - `[screaming]`

#### Expected Behavior:
1. **Volume Dip**: When loud caption appears, video volume should audibly drop to ~30%
2. **Visual Indicator**: Orange notification "🔉 Crest: Volume Lowered" appears top-right
3. **Volume Restore**: After 3 seconds, volume returns to original level
4. **Console Logs**: Check DevTools console for Crest activity logs

## Verification Checklist

### ✅ Core Functionality
- [ ] Flask server responds to GET /data with "Hello"
- [ ] Extension loads without errors in Chrome
- [ ] Content script injects on YouTube pages
- [ ] Subtitle observer detects caption changes
- [ ] AI analysis processes subtitle text
- [ ] Volume control works (audible dip and restore)
- [ ] Visual feedback appears during volume changes

### ✅ Observability (Datadog Dashboard)
- [ ] **Traces**: `/data` endpoint traces appear in APM
- [ ] **Logs**: Structured JSON logs with AI decisions
- [ ] **Metrics**: Custom metrics firing:
  - `crest.requests.total`
  - `crest.ai.requests.total`
  - `crest.ai.decision.yes` (when loud event detected)
  - `crest.ai.decision.no` (when no loud event)
  - `crest.processing.duration`

### ✅ Error Handling
- [ ] Server handles missing subtitle text gracefully
- [ ] Extension handles server connection failures
- [ ] AI errors don't crash the system
- [ ] CORS works without browser errors

## Troubleshooting

### Common Issues:

**Extension Not Loading:**
- Check manifest.json syntax
- Verify service_worker.js filename matches manifest
- Check Chrome Extensions page for error messages

**No Volume Changes:**
- Ensure captions are enabled on YouTube
- Check browser console for Crest logs
- Verify video element is found by content script

**Server Connection Errors:**
- Confirm Flask server is running on port 5000
- Check CORS configuration
- Verify host_permissions in manifest.json

**Missing Datadog Data:**
- Ensure DD_AGENT_HOST points to running Datadog agent
- Check environment variables are set
- Verify ddtrace-run is used to start server

## Success Criteria

The integration is successful when:
1. **User Experience**: Volume automatically lowers during loud captions and restores smoothly
2. **Technical**: All components communicate without errors
3. **Observability**: Full trace/log/metric data flows to Datadog
4. **Reliability**: System handles edge cases gracefully

## Demo Script

For demonstration purposes:

1. Start server: `ddtrace-run python app.py`
2. Load extension in Chrome
3. Navigate to: https://www.youtube.com/watch?v=dQw4w9WgXcQ (or any video with captions)
4. Enable closed captions
5. Wait for loud sound effects in captions
6. Show volume reduction + visual indicator
7. Display Datadog dashboard with real-time metrics

This completes the full-stack integration of Project Crest! 🎉