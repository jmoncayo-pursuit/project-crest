# Technology Stack & Build System

## Core Architecture
- **Backend**: Python Flask server with CORS enabled
- **Frontend**: Chrome Extension (Manifest V3)
- **AI Processing**: OpenAI via TrueFoundry AI Gateway
- **Observability**: Datadog APM, logging, and custom metrics

## Python Dependencies
```
flask
flask-cors
openai
ddtrace
datadog
python-json-logger
```

## Chrome Extension Structure
- `manifest.json` - Manifest V3 configuration
- `service-worker.js` - Background event coordinator
- `content-script.js` - YouTube page interaction

## Required Environment Variables
```bash
# TrueFoundry AI Gateway
TRUEFOUNDRY_API_KEY="tfy-..."
TRUEFOUNDRY_BASE_URL="https://..."

# Datadog Observability
DD_AGENT_HOST="localhost"
DD_LOGS_INJECTION="true"
DD_SERVICE="crest-agent"
DD_ENV="development"
DD_VERSION="0.1.0"
```

## Common Commands

### Development Server
```bash
# Start Flask server with Datadog tracing
ddtrace-run python app.py

# Basic development (without observability)
python app.py
```

### Chrome Extension
- Load unpacked extension from `chrome-extension/` directory
- Enable Developer mode in Chrome Extensions page
- Test on YouTube videos with subtitles

### Testing
- Manual end-to-end testing on YouTube
- Server communication via `http://localhost:5003/data`
- Datadog dashboard monitoring for traces/metrics

## Key Technical Constraints
- Chrome Extension must handle YouTube SPA navigation
- CORS configuration required for localhost communication
- All OpenAI calls must route through TrueFoundry Gateway
- Datadog instrumentation via `ddtrace-run` launcher