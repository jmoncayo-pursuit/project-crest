# Project Crest 🎵

AI-powered Chrome browser extension that automatically adjusts YouTube video volume to prevent jarring loud moments. Uses real-time audio analysis and AI to create a pleasant, consistent listening experience.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser
- OpenAI API key (optional, works in mock mode without)

### 1. Start the Server
```bash
# Install dependencies
pip install flask flask-cors openai ddtrace datadog python-json-logger

# Start the Flask server
python app.py
```

### 2. Load Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `chrome-extension/` folder
5. The Crest icon should appear in your extensions

### 3. Test on YouTube
1. Go to any YouTube video
2. The extension will automatically start monitoring
3. **Watch the extension icon** - it turns green when actively managing volume
4. **Click the extension icon** to see the live activity dashboard
5. Look for "Crest Audio Agent" messages in browser console (F12)
6. Loud events will trigger automatic volume reduction

## 🏗️ Architecture

### Components
- **Flask Server** (`app.py`) - AI processing and decision engine
- **Chrome Extension** - Real-time audio monitoring and volume control
- **Content Script** - Injected into YouTube pages for audio analysis
- **Service Worker** - Coordinates between content script and server

### AI Integration
- **Live Mode**: Uses OpenAI via TrueFoundry AI Gateway for intelligent decisions
- **Mock Mode**: Rule-based detection when API keys aren't available
- **Observability**: Full Datadog integration for monitoring and metrics

## 🔧 Configuration

### Environment Variables
```bash
# TrueFoundry AI Gateway (optional)
TRUEFOUNDRY_API_KEY="tfy-..."
TRUEFOUNDRY_BASE_URL="https://..."

# Datadog Observability (optional)
DD_AGENT_HOST="localhost"
DD_SERVICE="crest-agent"
DD_ENV="development"
```

### Extension Settings
The extension automatically detects:
- Audio volume spikes (>30% above baseline)
- Subtitle-based loud events `[explosion]`, `[gunshot]`, etc.
- User volume corrections for learning

## 🧪 Testing

### Server Tests
```bash
# Test all endpoints
python test_live_system.py

# Simple server test
python test_server.py
```

### Manual Testing
1. Load extension in Chrome
2. Go to YouTube video with dynamic audio
3. Check browser console for agent messages
4. Verify volume adjustments during loud scenes

## 📁 Project Structure

```
├── app.py                    # Main Flask server
├── chrome-extension/         # Chrome extension files
│   ├── manifest.json        # Extension configuration
│   ├── service_worker.js    # Background coordination
│   └── content-script-*.js  # YouTube page interaction
├── test_*.py                # Testing utilities
├── .kiro/specs/             # Feature specifications
└── requirements.txt         # Python dependencies
```

## 🎯 Key Features

- **Real-time Audio Analysis**: Monitors audio levels and detects sudden spikes
- **AI-Enhanced Detection**: Uses OpenAI to confirm loud events intelligently
- **Proactive Volume Control**: Adjusts volume before loud moments occur
- **Visual Dashboard**: Extension popup shows live activity log and statistics
- **Smart Icon Feedback**: Extension icon changes color when actively managing volume
- **User Learning**: Tracks user corrections to improve accuracy
- **Production Ready**: Full observability with Datadog integration

## 🎛️ Extension Dashboard

The Chrome extension includes a comprehensive dashboard accessible by clicking the extension icon:

### Features:
- **Live Activity Log**: Real-time feed of all agent actions
- **Statistics**: Volume adjustment count and last action timestamp
- **Status Indicator**: Shows when agent is actively monitoring vs. managing volume
- **Visual Feedback**: Extension icon changes from gray (monitoring) to green (active)
- **Persistent History**: Activity log saved between browser sessions

### Dashboard Shows:
- `🎵 Agent lowered volume to 25% for 3s`
- `🔊 Audio spike detected! Volume lowered to 25%`
- Timestamps and detailed action history
- Performance statistics for demo purposes

## 🔍 Troubleshooting

### Extension Not Working
1. Check if server is running on port 5003
2. Verify extension is loaded and enabled
3. **Check extension dashboard** for activity logs
4. Look for icon color changes (gray → green)
5. Check browser console for error messages

### Server Issues
1. Check port 5003 isn't in use: `lsof -i :5003`
2. Verify Python dependencies are installed
3. Check server logs for errors
4. Test endpoints with `curl http://localhost:5003/health`

## 🏆 Hackathon Context

Built for NYC AI Agents Hackathon showcasing:
- **OpenAI**: Intelligent loud event detection
- **TrueFoundry**: AI Gateway for API management  
- **Datadog**: Complete observability and monitoring
- **Chrome Extensions**: Real-time browser integration

## 📊 Metrics & Observability

The system tracks:
- `crest.loud_event.detected` - Loud events found
- `crest.user_correction.count` - User disagreements (key metric)
- `crest.ai.requests.total` - AI API usage
- `crest.processing.duration` - Response times

## 🤝 Contributing

This is a hackathon project focused on demonstrating AI agent capabilities with production-grade observability. The architecture prioritizes rapid development while maintaining monitoring best practices.

---

*Project Crest - Making YouTube audio pleasant, one intelligent adjustment at a time* 🎵