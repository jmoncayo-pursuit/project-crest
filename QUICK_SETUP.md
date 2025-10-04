# Quick Setup Guide for Project Crest

## 1. Environment Setup (Optional for Demo)

### Option A: Mock Mode (No Credentials Needed)
Just start the server directly - it will automatically run in Mock Mode:
```bash
python start_crest.py
```
✅ **Perfect for demos and testing!**

### Option B: Live Mode (Requires Credentials)
Copy and configure environment file:
```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:
```bash
# TrueFoundry AI Gateway (Required for Live Mode)
TRUEFOUNDRY_API_KEY=tfy-your-actual-api-key
TRUEFOUNDRY_BASE_URL=https://your-actual-truefoundry-endpoint

# Datadog Observability Configuration (Pre-configured)
DD_SERVICE=crest-agent
DD_ENV=development
DD_VERSION=0.1.0
DD_LOGS_INJECTION=true
DD_AGENT_HOST=localhost
```

Load environment variables:
```bash
source setup_env_from_file.sh
```

## 2. Start the System

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Start the Flask server:
```bash
python start_crest.py
```

### Load Chrome extension:
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension/` folder

## 3. Test the Integration

### Test Mock Mode (Recommended First):
```bash
python test_mock_mode.py
```

### Navigate to YouTube video with captions
Look for loud event captions like:
- `[explosion]` ✅ Triggers volume reduction
- `[gunshot]` ✅ Triggers volume reduction  
- `[dramatic music]` ✅ Triggers volume reduction
- `[thunder]` ✅ Triggers volume reduction
- `[crash]` ✅ Triggers volume reduction
- `"Hello there"` ❌ No volume change

### Expected behavior:
- Volume automatically lowers to 30% when loud caption appears
- Orange notification shows "🔉 Crest: Volume Lowered"
- Volume restores after 5 seconds

## 4. Verification Checklist

- [ ] Server starts without errors
- [ ] Extension loads in Chrome
- [ ] Volume control works on YouTube
- [ ] Datadog traces appear (if agent running)
- [ ] Console shows AI decisions (YES/NO)
- [ ] **NEW**: User feedback loop works (manually adjust volume after agent changes it)

## 🔄 Adaptive Agent Features

### Feedback Loop (Creative Eval):
1. **Agent Action**: Lowers volume on loud captions
2. **User Correction**: User manually adjusts volume
3. **Feedback Detection**: Extension detects user correction
4. **Metric Recording**: Sends `crest.user_correction.count` to Datadog
5. **Continuous Learning**: Creates data for future improvements

### Test the Feedback Loop:
```bash
python test_feedback_loop.py
```

## Mode Comparison

| Feature | Mock Mode | Live Mode |
|---------|-----------|-----------|
| **Setup** | No credentials needed | Requires TrueFoundry API key |
| **AI Logic** | Rule-based keywords | Real OpenAI analysis |
| **Speed** | Instant response | ~1-2 second API call |
| **Accuracy** | Good for common cases | Superior AI understanding |
| **Demo Ready** | ✅ Perfect | ✅ Production quality |

## Troubleshooting

**Server won't start**: Check if port 5000 is available
**Extension not working**: Check Chrome DevTools console for errors
**No volume changes**: Ensure YouTube captions are enabled
**Want Live Mode**: Set TrueFoundry credentials in `.env` file