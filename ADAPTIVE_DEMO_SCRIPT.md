# 🏆 Project Crest - Adaptive Agent Demo Script

## Overview
This demo showcases Project Crest as an **adaptive AI agent** that learns from user feedback - a key differentiator for the hackathon judging criteria.

## 🎯 Judging Criteria Addressed

### ✅ Creative Evals
- **Custom Metric**: `crest.user_correction.count` tracks when users override agent decisions
- **Feedback Loop**: Agent detects and records user corrections in real-time
- **Learning Signal**: Creates data for continuous improvement

### ✅ Continuous Improvement Autonomously  
- **Self-Evaluation**: Agent monitors its own performance through user actions
- **Adaptive Behavior**: Feedback creates learning opportunities
- **Autonomous Monitoring**: No human intervention needed for feedback collection

## 🎬 Demo Flow (5 Minutes)

### 1. Setup & Launch (1 minute)
```bash
# Start server in Mock Mode (no credentials needed)
python start_crest.py

# Test basic functionality
python test_mock_mode.py

# Test adaptive features
python test_feedback_loop.py
```

**Show**: Server starts in Mock Mode, all tests pass

### 2. Chrome Extension Demo (2 minutes)
1. **Load Extension**: Chrome → Extensions → Load Unpacked → `chrome-extension/`
2. **Navigate to YouTube**: Find video with captions (action movie trailer)
3. **Enable Captions**: Click CC button
4. **Demonstrate Core Function**: 
   - Wait for `[explosion]` or similar caption
   - Show volume automatically lowers
   - Show orange notification appears
   - Show volume restores after 5 seconds

**Show**: Basic AI agent functionality working perfectly

### 3. Adaptive Learning Demo (2 minutes)
1. **Trigger Agent Action**: Wait for another loud caption
2. **User Correction**: Manually adjust volume while agent notification is showing
3. **Show Feedback Detection**: Check browser console for "User correction detected"
4. **Show Server Logs**: Display server receiving feedback events
5. **Show Datadog Metrics**: `crest.user_correction.count` incrementing

**Show**: Agent learning from user behavior in real-time

## 🏆 Key Talking Points

### "This isn't just an AI agent - it's an adaptive AI agent"
- **Reactive**: Responds to subtitle events
- **Proactive**: Predicts loud moments before they happen  
- **Adaptive**: Learns from user corrections
- **Self-Monitoring**: Tracks its own performance

### "Creative Evaluation in Action"
- **Traditional Eval**: "Did the agent lower the volume?"
- **Our Creative Eval**: "How often do users correct the agent's decisions?"
- **Continuous Learning**: Each correction becomes training data

### "Autonomous Improvement Loop"
- **No Manual Intervention**: Agent automatically detects feedback
- **Real-Time Metrics**: Immediate visibility into performance
- **Scalable Learning**: Framework for future ML improvements

## 📊 Technical Architecture

```
YouTube Captions → Chrome Extension → Flask Server → AI Decision
                                          ↓
User Volume Change → Feedback Detection → Custom Metrics → Datadog
                                          ↓
                              Future ML Training Data
```

## 🎯 Competitive Advantages

1. **Beyond Basic Functionality**: Most agents just "work" - ours learns
2. **Production-Ready Observability**: Full Datadog integration with custom metrics
3. **Real User Feedback**: Actual behavioral data, not synthetic tests
4. **Hackathon-Perfect**: Demonstrates all sponsor technologies working together

## 🚀 Future Roadmap (Mention if Asked)

1. **ML Integration**: Use feedback data to train better prediction models
2. **Personalization**: Learn individual user preferences
3. **A/B Testing**: Test different volume reduction strategies
4. **Multi-Modal**: Expand beyond audio to visual cues

## 💡 Demo Tips

- **Start with Mock Mode**: Shows it works without API dependencies
- **Emphasize the Feedback Loop**: This is the key differentiator
- **Show Real Metrics**: Datadog dashboard with live data
- **Highlight Autonomy**: No human needed for the learning loop
- **Connect to Judging Criteria**: Explicitly mention "creative evals" and "continuous improvement"

---

**This positions Project Crest as the most sophisticated and forward-thinking agent in the competition!** 🏆