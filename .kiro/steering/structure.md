# Project Structure & Organization

## Root Directory Layout
```
├── app.py                    # Main Flask server application
├── requirements.txt          # Python dependencies
├── README.md                # Project overview and setup
├── SPECS_*.md               # Detailed technical specifications
├── TESTING_INSTRUCTIONS.md  # Manual testing procedures
├── chrome-extension/        # Chrome extension components
└── .kiro/                   # Kiro IDE configuration and specs
```

## Chrome Extension Structure
```
chrome-extension/
├── manifest.json           # Extension configuration (Manifest V3)
├── service-worker.js       # Background script for coordination
└── content-script.js       # Injected script for YouTube interaction
```

## Flask Server Organization
- **Single file approach**: `app.py` contains all server logic
- **Minimal structure**: Focus on hackathon MVP, not production architecture
- **Key components**:
  - CORS configuration for Chrome extension
  - `/data` endpoint for subtitle processing
  - AI gateway integration (TrueFoundry → OpenAI)
  - Datadog observability instrumentation

## Specification Files
- `SPECS_LOCAL_AGENT.md` - Python server implementation details
- `SPECS_CHROME_EXTENSION.md` - Extension architecture and code
- `TESTING_INSTRUCTIONS.md` - Manual testing procedures

## Kiro Configuration
```
.kiro/
├── steering/               # AI assistant guidance rules
└── specs/                 # Feature specifications and tasks
    └── observability-ai-integration/
        ├── requirements.md # MVP requirements
        ├── design.md      # Architecture design
        └── tasks.md       # Implementation roadmap
```

## Development Workflow
1. **Backend First**: Start Flask server with basic communication
2. **Extension Integration**: Build Chrome extension components
3. **AI Pipeline**: Add TrueFoundry and OpenAI integration
4. **Observability**: Instrument with Datadog tracing/metrics
5. **End-to-End Testing**: Verify complete YouTube workflow

## File Naming Conventions
- Specification files: `SPECS_*.md` (uppercase)
- Chrome extension: kebab-case filenames
- Python: snake_case following PEP 8
- Configuration: lowercase with extensions