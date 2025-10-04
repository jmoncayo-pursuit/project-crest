# 🚀 Crest Demo Startup Guide

## Quick Start (3 steps)

### 1. Start the Server
```bash
# Recommended: Loads environment and starts server
python start_demo.py

# Alternative: Direct start (mock mode only)
python app_minimal.py
```

### 2. Load Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `chrome-extension/` folder from this project
5. You should see "Project Crest" extension loaded

### 3. Test on YouTube
1. Go to any YouTube video with captions/subtitles
2. Enable captions (CC button)
3. Look for videos with action scenes, explosions, or dramatic music
4. Watch for:
   - **Icon changes**: Extension icon flashes from gray to colored when detecting loud events
   - **Volume changes**: Audio automatically lowers during loud moments
   - **Console logs**: Check browser DevTools console for activity

## 🧪 Testing Your Setup

Run the complete system test:
```bash
python test_complete_system.py
```

This will verify:
- ✅ Server is running and healthy
- ✅ AI processing works for different subtitle types
- ✅ Chrome extension endpoints respond
- ✅ Environment variables are set

## 🎯 Hackathon Demo Points

### Core Functionality
- **AI-Powered Detection**: Uses OpenAI via TrueFoundry to analyze subtitle text
- **Proactive Volume Control**: Lowers volume BEFORE loud sounds play
- **Smart Recognition**: Detects patterns like "[explosion]", "[gunshot]", "[dramatic music]"

### Technical Integration
- **OpenAI via TrueFoundry**: AI Gateway for intelligent subtitle analysis
- **Datadog**: Full observability with APM, metrics, and logging
- **Chrome Extension**: Real-time browser integration with YouTube
- **Flask Backend**: High-performance API server with CORS support

### Visual Feedback
- **Icon Animation**: Extension icon changes color when active
- **Real-time Processing**: Instant response to subtitle changes
- **User Correction Tracking**: Logs when users manually adjust volume

## 🔧 Troubleshooting

### Server Issues
```bash
# Check if server is running
curl http://localhost:5003/health

# Test AI processing
curl -X POST http://localhost:5003/data \
  -H "Content-Type: application/json" \
  -d '{"text": "[explosion]"}'
```

### Chrome Extension Issues
1. **Check Console**: Open DevTools → Console tab for error messages
2. **Reload Extension**: Go to chrome://extensions/ and click reload
3. **Check Permissions**: Ensure localhost:5003 is allowed in manifest
4. **Test on Different Videos**: Some YouTube videos don't have subtitle data

### Icon Not Changing
- Verify extension is loaded and active
- Check that subtitle text contains detectable patterns
- Look for console messages in DevTools

## 📊 Demo Script

1. **Show the Problem**: Play a YouTube video with sudden loud moments
2. **Load Extension**: Demonstrate loading the Chrome extension
3. **Show AI Detection**: Open DevTools console to show real-time processing
4. **Demonstrate Volume Control**: Show automatic volume reduction during loud scenes
5. **Show Observability**: Display Datadog dashboard with metrics and traces
6. **Explain AI Pipeline**: TrueFoundry → OpenAI → Smart Detection → Volume Control

## 🎉 Success Indicators

- Extension icon flashes during loud events
- Volume automatically reduces during detected loud moments
- Console shows successful API calls to localhost:5003
- Datadog receives metrics and traces
- AI correctly identifies loud vs normal subtitle text

Your Crest agent is ready for the hackathon demo! 🏆