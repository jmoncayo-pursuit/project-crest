# 🎯 Project Crest - Final Demo Checklist

## 🚀 Quick Start (5 Minutes)

### 1. Environment Setup
```bash
# Set required environment variables
export TRUEFOUNDRY_API_KEY="your-truefoundry-key"
export TRUEFOUNDRY_BASE_URL="your-truefoundry-endpoint"

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Full Stack
```bash
# Option A: Use the startup script (recommended)
python start_crest.py

# Option B: Manual start with Datadog tracing
ddtrace-run python app.py
```

### 3. Load Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `chrome-extension/` folder
4. Verify "Project Crest" appears in extensions list

### 4. Test Integration
```bash
# Run integration tests
python test_integration.py
```

## 🎬 Live Demo Script

### Demo Video Suggestions:
- **Action Movie Trailer**: "Avengers Endgame trailer" - multiple explosions
- **Gaming Content**: "Call of Duty gameplay" - gunshots and explosions  
- **Movie Clips**: "Movie explosion compilation" - dramatic sound effects

### Demo Steps:
1. **Show Backend**: Display terminal with server running and logs
2. **Show Extension**: Chrome extensions page with Project Crest loaded
3. **Navigate to YouTube**: Go to video with captions (suggest specific video)
4. **Enable Captions**: Click CC button, show captions are visible
5. **Wait for Loud Event**: Look for captions like `[explosion]`, `[gunshot]`
6. **Demonstrate Volume Control**: 
   - Point out when loud caption appears
   - Show volume visibly/audibly drops
   - Show orange notification: "🔉 Crest: Volume Lowered"
   - Show volume restores after 3 seconds
7. **Show Observability**: Display Datadog dashboard with:
   - APM traces for `/data` endpoint
   - Structured logs with AI decisions
   - Custom metrics: `crest.loud_event.detected`

## ✅ Success Criteria Checklist

### Core Functionality
- [ ] Flask server starts without errors
- [ ] Chrome extension loads successfully  
- [ ] Extension detects YouTube subtitle changes
- [ ] AI analyzes subtitle text for loud events
- [ ] Volume automatically lowers during loud captions
- [ ] Volume restores after 3 seconds
- [ ] Visual feedback appears during volume changes
- [ ] No CORS errors in browser console

### Observability (Datadog)
- [ ] APM traces appear for `/data` endpoint calls
- [ ] Structured JSON logs show AI decision process
- [ ] Custom metrics fire:
  - `crest.requests.total`
  - `crest.ai.requests.total` 
  - `crest.ai.decision.yes` (loud events)
  - `crest.ai.decision.no` (normal content)
- [ ] Processing duration metrics recorded
- [ ] Error metrics tracked for failures

### Integration Points
- [ ] **OpenHands**: Agent orchestration (this implementation)
- [ ] **TrueFoundry**: AI Gateway for OpenAI calls
- [ ] **OpenAI**: GPT analysis of subtitle text
- [ ] **Datadog**: Full observability stack
- [ ] **Structify**: Text processing (integrated in AI pipeline)

## 🐛 Troubleshooting Quick Fixes

### Server Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Check environment variables
echo $TRUEFOUNDRY_API_KEY
echo $TRUEFOUNDRY_BASE_URL

# Start without Datadog if needed
python app.py
```

### Extension Issues
- Reload extension in Chrome extensions page
- Check browser console for errors
- Verify manifest.json syntax with: `python -c "import json; json.load(open('chrome-extension/manifest.json'))"`

### No Volume Changes
- Ensure YouTube captions are enabled (CC button)
- Check browser console for "Crest:" messages
- Verify video element exists: `document.querySelector('video')`

### Missing Datadog Data
- Ensure Datadog agent running on localhost:8125
- Start server with `ddtrace-run python app.py`
- Check DD_* environment variables are set

## 🎉 Demo Success Indicators

**Visual Cues:**
- Orange notification appears: "🔉 Crest: Volume Lowered"
- Console logs show: "Crest: Lowering volume from X to Y"
- Datadog dashboard shows real-time metrics

**Audio Cues:**
- Audible volume reduction during loud captions
- Smooth volume restoration after 3 seconds

**Technical Validation:**
- Server logs show AI decisions in JSON format
- Browser DevTools show successful API calls
- Datadog APM traces appear within seconds

## 📊 Key Metrics to Highlight

1. **Response Time**: AI analysis completes in <2 seconds
2. **Accuracy**: AI correctly identifies loud vs normal content
3. **User Experience**: Seamless volume control without user intervention
4. **Observability**: 100% trace coverage with structured logging
5. **Reliability**: Graceful error handling and fallbacks

This completes the full-stack integration of Project Crest! 🚀