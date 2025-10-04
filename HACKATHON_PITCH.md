# 🎯 Project Crest - Hackathon Demo Pitch

## 🚀 **The Problem**
YouTube videos have jarring volume spikes that hurt your ears and disturb others. Current solutions are reactive - you adjust volume AFTER the loud moment hits.

## 🧠 **Our AI Solution**
**Crest is a proactive AI agent** that reads YouTube subtitles in real-time and automatically lowers volume BEFORE loud events happen.

## ⚡ **Live Demo Flow**

### 1. **Show the Problem** (30 seconds)
- Play YouTube video with sudden explosion/gunshot
- "Ouch! That hurt my ears and probably woke up my neighbors"

### 2. **Load Crest Extension** (30 seconds)  
- Install Chrome extension from `chrome-extension/` folder
- Show it's now active in browser toolbar

### 3. **Show AI in Action** (60 seconds)
- Same video, but now Crest is active
- **Watch the magic**: Volume automatically lowers during loud scenes
- **Visual feedback**: Extension icon flashes when AI detects loud events
- **Show console**: Real-time AI processing logs

### 4. **Explain the AI Pipeline** (60 seconds)
```
YouTube Subtitles → Chrome Extension → Flask API → 
TrueFoundry Gateway → OpenAI GPT-4 → Smart Decision → 
Volume Control + Datadog Metrics
```

## 🏆 **Technical Achievements**

### **Real AI Intelligence**
- **OpenAI via TrueFoundry**: Analyzes subtitle text like "[explosion]", "[gunshot]", "[dramatic music]"
- **Smart Decisions**: Distinguishes loud events from normal speech
- **Sub-second Response**: ~500-1000ms processing time

### **Production-Ready Observability**  
- **Datadog Integration**: APM traces, custom metrics, structured logging
- **User Feedback Loop**: Tracks when users manually adjust volume
- **Error Handling**: Graceful fallbacks and comprehensive monitoring

### **Seamless User Experience**
- **Chrome Extension**: Works on any YouTube video with captions
- **Zero Configuration**: Install and it just works
- **Visual Feedback**: Icon changes show when AI is actively protecting your ears

## 📊 **Demo Results You'll See**

**Loud Events Detected & Volume Lowered:**
- `[explosion]` → Volume to 30% for 5 seconds
- `[gunshot]` → Volume to 30% for 5 seconds  
- `[dramatic music]` → Volume to 30% for 5 seconds
- `[applause]` → Volume to 30% for 5 seconds

**Normal Speech Ignored:**
- "Hello everyone, welcome to my channel" → No change
- "Today we're going to learn about..." → No change

## 🎯 **Why This Matters for Hackathon**

### **Real AI Agent Behavior**
- Makes intelligent decisions in real-time
- Learns from user feedback
- Proactive rather than reactive

### **Production Technology Stack**
- **TrueFoundry AI Gateway**: Enterprise AI infrastructure
- **Datadog Observability**: Production monitoring and metrics
- **Modern Web Extension**: Manifest V3 Chrome extension

### **Immediate User Value**
- Solves a real problem everyone has experienced
- Works seamlessly without user intervention
- Protects hearing and prevents disturbing others

## 🚀 **Ready to Demo!**

```bash
# Start the AI server
python start_demo.py

# Load Chrome extension from chrome-extension/ folder
# Go to YouTube video with captions
# Watch Crest protect your ears! 🎧
```

**Your AI agent is live, intelligent, and ready to impress the judges!** 🏆