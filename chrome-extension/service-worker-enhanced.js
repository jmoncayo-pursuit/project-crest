// service-worker-enhanced.js - Enhanced with detailed activity logging and dashboard support

// Icon state management
const IconState = {
    DEFAULT: {
        "128": "data:image/svg+xml;base64," + btoa(`
            <svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
                <rect width="128" height="128" rx="20" fill="#6c757d"/>
                <text x="64" y="80" text-anchor="middle" fill="white" font-size="48" font-family="Arial">C</text>
            </svg>
        `)
    },
    ACTIVE: {
        "128": "data:image/svg+xml;base64," + btoa(`
            <svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
                <rect width="128" height="128" rx="20" fill="#28a745"/>
                <text x="64" y="80" text-anchor="middle" fill="white" font-size="48" font-family="Arial">C</text>
            </svg>
        `)
    },
    ERROR: {
        "128": "data:image/svg+xml;base64," + btoa(`
            <svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
                <rect width="128" height="128" rx="20" fill="#dc3545"/>
                <text x="64" y="80" text-anchor="middle" fill="white" font-size="48" font-family="Arial">C</text>
            </svg>
        `)
    }
};

// Enhanced dashboard manager
class DashboardManager {
    constructor() {
        this.events = [];
        this.stats = {
            totalAdjustments: 0,
            subtitleDetections: 0,
            audioDetections: 0,
            userCorrections: 0,
            lastActionTime: null,
            accuracyRate: 0,
            sessionStartTime: Date.now()
        };
        this.activeTabs = new Set();
    }

    logEvent(eventData) {
        const event = {
            ...eventData,
            timestamp: Date.now(),
            id: Date.now() + Math.random()
        };

        this.events.unshift(event);

        // Keep only last 50 events
        if (this.events.length > 50) {
            this.events = this.events.slice(0, 50);
        }

        this.updateStats(event);
        this.broadcastToPopup(event);

        console.log('📊 Dashboard Event:', event);
    }

    updateStats(event) {
        if (event.type === 'volume_adjustment') {
            this.stats.totalAdjustments++;
            this.stats.lastActionTime = event.timestamp;

            if (event.trigger === 'subtitle') {
                this.stats.subtitleDetections++;
            } else if (event.trigger === 'audio') {
                this.stats.audioDetections++;
            }
        } else if (event.type === 'user_correction') {
            this.stats.userCorrections++;
        }

        // Calculate accuracy rate (inverse of correction rate)
        const totalActions = this.stats.totalAdjustments;
        this.stats.accuracyRate = totalActions > 0
            ? Math.max(0, (totalActions - this.stats.userCorrections) / totalActions)
            : 1.0;
    }

    broadcastToPopup(event) {
        chrome.runtime.sendMessage({
            type: 'DASHBOARD_UPDATE',
            event: event,
            stats: this.stats
        }).catch(() => {
            // Popup might not be open, ignore error
        });

        // Also send simple LOG_EVENT for compatibility with basic popup
        if (event.message) {
            chrome.runtime.sendMessage({
                type: 'LOG_EVENT',
                text: event.message
            }).catch(() => {
                // Popup might not be open, ignore error
            });
        }
    }

    getStats() {
        return {
            ...this.stats,
            sessionDuration: Date.now() - this.stats.sessionStartTime
        };
    }
}

const dashboardManager = new DashboardManager();

// Enhanced navigation handling
chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    if (details.url?.includes("youtube.com/watch")) {
        console.log('🔄 Injecting enhanced content script into YouTube tab');

        chrome.scripting.executeScript({
            target: { tabId: details.tabId },
            files: ["content-script-enhanced-audio.js"]
        }).then(() => {
            dashboardManager.logEvent({
                type: 'script_injection',
                message: 'Enhanced content script injected',
                tabId: details.tabId,
                url: details.url
            });
        }).catch(error => {
            console.error('Script injection failed:', error);
            dashboardManager.logEvent({
                type: 'error',
                message: `Script injection failed: ${error.message}`,
                tabId: details.tabId
            });
        });
    }
});

// Enhanced message handling
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('📨 Service Worker received message:', message.type);

    // Handle real-time audio data
    if (message.type === 'AUDIO_DATA') {
        handleAudioData(message.data, sender);
    }
    // Handle subtitle data
    else if (message.type === 'SUBTITLE_DATA') {
        handleSubtitleData(message.text, sender);
    }
    // Handle user corrections
    else if (message.type === 'USER_CORRECTION') {
        handleUserCorrection(sender);
    }
    // Handle popup requests for dashboard data
    else if (message.type === 'GET_DASHBOARD_DATA') {
        sendResponse({
            events: dashboardManager.events,
            stats: dashboardManager.getStats()
        });
        return true;
    }
    // Handle legacy volume lowered events
    else if (message.type === 'VOLUME_LOWERED') {
        handleVolumeLowered(message.data, sender);
    }

    return true;
});

async function handleAudioData(audioData, sender) {
    try {
        console.log('🔊 Processing audio data:', audioData);

        const response = await fetch('http://localhost:5003/audio-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                volume: audioData.volume,
                baseline: audioData.baseline,
                spike: audioData.spike,
                timestamp: audioData.timestamp
            }),
        });

        const data = await response.json();

        if (data.action === 'LOWER_VOLUME') {
            // Apply volume reduction
            setIconActive(sender.tab.id);
            chrome.tabs.sendMessage(sender.tab.id, {
                action: 'LOWER_VOLUME',
                level: data.level,
                duration: data.duration,
                confidence: data.confidence,
                trigger: 'audio'
            });

            // Log detailed event
            dashboardManager.logEvent({
                type: 'volume_adjustment',
                trigger: 'audio',
                confidence: data.confidence,
                level: data.level,
                duration: data.duration,
                message: `🔊 Audio spike detected (${(audioData.spike * 100).toFixed(1)}% above baseline)`,
                audioData: {
                    volume: audioData.volume,
                    baseline: audioData.baseline,
                    spike: audioData.spike
                },
                aiReasoning: `Volume spike of ${audioData.spike.toFixed(3)} detected above baseline ${audioData.baseline.toFixed(3)}`
            });

            // Reset icon after duration
            setTimeout(() => {
                setIconDefault(sender.tab.id);
            }, data.duration + 500);
        } else {
            // Log non-action for debugging
            dashboardManager.logEvent({
                type: 'audio_analysis',
                trigger: 'audio',
                confidence: data.confidence,
                message: `🔇 Audio analyzed - no action needed (spike: ${(audioData.spike * 100).toFixed(1)}%)`,
                audioData: audioData
            });
        }

    } catch (error) {
        console.error('🚨 Audio processing error:', error);
        setIconError(sender.tab.id);

        dashboardManager.logEvent({
            type: 'error',
            message: `Audio processing failed: ${error.message}`,
            trigger: 'audio'
        });

        setTimeout(() => setIconDefault(sender.tab.id), 2000);
    }
}

async function handleSubtitleData(subtitleText, sender) {
    try {
        console.log('📝 Processing subtitle:', subtitleText);

        const response = await fetch('http://localhost:5003/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: subtitleText }),
        });

        const data = await response.json();

        if (data.action === 'LOWER_VOLUME') {
            // Apply volume reduction
            setIconActive(sender.tab.id);
            chrome.tabs.sendMessage(sender.tab.id, {
                action: 'LOWER_VOLUME',
                level: data.level,
                duration: data.duration,
                confidence: data.confidence || 0.8,
                trigger: 'subtitle'
            });

            // Log detailed event
            dashboardManager.logEvent({
                type: 'volume_adjustment',
                trigger: 'subtitle',
                confidence: data.confidence || 0.8,
                level: data.level,
                duration: data.duration,
                message: `📝 Subtitle detected loud event: "${subtitleText}"`,
                subtitleText: subtitleText,
                aiReasoning: `AI detected loud event in subtitle: "${subtitleText}"`
            });

            // Reset icon after duration
            setTimeout(() => {
                setIconDefault(sender.tab.id);
            }, data.duration + 500);
        } else {
            // Log analysis for debugging
            dashboardManager.logEvent({
                type: 'subtitle_analysis',
                trigger: 'subtitle',
                confidence: data.confidence || 0.8,
                message: `📝 Subtitle analyzed: "${subtitleText}" - no action needed`,
                subtitleText: subtitleText
            });
        }

    } catch (error) {
        console.error('🚨 Subtitle processing error:', error);
        setIconError(sender.tab.id);

        dashboardManager.logEvent({
            type: 'error',
            message: `Subtitle processing failed: ${error.message}`,
            trigger: 'subtitle',
            subtitleText: subtitleText
        });

        setTimeout(() => setIconDefault(sender.tab.id), 2000);
    }
}

function handleUserCorrection(sender) {
    console.log('👤 User correction detected');

    // Send feedback to server
    fetch('http://localhost:5003/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ event: 'user_corrected_volume' }),
    }).catch(err => console.error('Feedback error:', err));

    // Log correction event
    dashboardManager.logEvent({
        type: 'user_correction',
        message: '👤 User manually adjusted volume (learning opportunity)',
        trigger: 'user'
    });
}

function handleVolumeLowered(data, sender) {
    console.log('🎵 Legacy volume lowered event:', data);

    setIconActive(sender.tab.id);

    dashboardManager.logEvent({
        type: 'volume_adjustment',
        trigger: 'legacy',
        level: data.level,
        duration: data.duration,
        message: `🎵 Volume lowered to ${data.level}% for ${data.duration / 1000}s`,
        confidence: 0.8
    });

    setTimeout(() => {
        setIconDefault(sender.tab.id);
    }, data.duration + 500);
}

// Enhanced icon management
function setIconActive(tabId) {
    try {
        chrome.action.setIcon({
            path: IconState.ACTIVE,
            tabId: tabId
        });
        dashboardManager.activeTabs.add(tabId);
    } catch (error) {
        console.error('Error setting active icon:', error);
    }
}

function setIconDefault(tabId) {
    try {
        chrome.action.setIcon({
            path: IconState.DEFAULT,
            tabId: tabId
        });
        dashboardManager.activeTabs.delete(tabId);
    } catch (error) {
        console.error('Error setting default icon:', error);
    }
}

function setIconError(tabId) {
    try {
        chrome.action.setIcon({
            path: IconState.ERROR,
            tabId: tabId
        });
    } catch (error) {
        console.error('Error setting error icon:', error);
    }
}

// Clean up when tabs are closed
chrome.tabs.onRemoved.addListener((tabId) => {
    dashboardManager.activeTabs.delete(tabId);
});

// Initialize dashboard
console.log('🚀 Enhanced Crest Service Worker initialized with dashboard support');
dashboardManager.logEvent({
    type: 'system',
    message: '🚀 Enhanced Crest AI Agent initialized',
    trigger: 'system'
});