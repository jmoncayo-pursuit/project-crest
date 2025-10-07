# Crest Architecture

Simple, clean architecture for AI-powered volume control.

## Core Components

### Backend (`app.py`)
- Flask server with AI integration
- Subtitle analysis endpoint (`/data`)
- Audio analysis endpoint (`/audio-data`)
- Caching and performance optimizations
- Datadog observability

### Chrome Extension
- **Content Script** (`content-script-enhanced-audio.js`)
  - Real-time audio monitoring with Web Audio API
  - Subtitle detection from YouTube captions
  - Smooth volume control with transitions
  - Dual detection coordination
  
- **Service Worker** (`service-worker-enhanced.js`)
  - Message coordination between content script and server
  - Enhanced logging and dashboard updates
  
- **Popup** (`popup-enhanced.html/js`)
  - Real-time dashboard with activity feed
  - Performance metrics and AI insights
  - Manual testing controls

## Data Flow

1. **Subtitle Detection**: Content script monitors YouTube captions
2. **Audio Monitoring**: Web Audio API analyzes real-time audio levels
3. **AI Analysis**: Server processes events through TrueFoundry → OpenAI
4. **Volume Control**: Smooth transitions based on AI confidence
5. **Dashboard**: Real-time updates with decision reasoning

## Key Features

- **Dual Detection**: Subtitle + audio analysis working together
- **Smart Coordination**: Prevents duplicate adjustments
- **Performance**: Caching, deduplication, fast fallbacks
- **Observability**: Datadog tracing, metrics, and logging
- **User Experience**: Smooth transitions, confidence-based adjustments

## Files Structure

```
├── app.py                                    # Flask server
├── chrome-extension/
│   ├── manifest.json                         # Extension config
│   ├── content-script-enhanced-audio.js      # Main content script
│   ├── service-worker-enhanced.js            # Background coordination
│   ├── popup-enhanced.html                   # Dashboard UI
│   ├── popup-enhanced.js                     # Dashboard logic
│   └── content-script-simple-working.js      # Fallback simple version
├── test_system.py                            # Simple comprehensive test
├── test_ai_integration.py                    # AI-specific tests
├── test_integration.py                       # Integration tests
└── README.md                                 # Setup instructions
```

## Testing

- `test_system.py` - Main test suite (subtitle, audio, performance)
- `test_ai_integration.py` - AI-specific validation
- `test_integration.py` - End-to-end integration

## Setup

1. Start server: `ddtrace-run python app.py`
2. Load extension from `chrome-extension/` folder
3. Test on YouTube videos with dynamic audio