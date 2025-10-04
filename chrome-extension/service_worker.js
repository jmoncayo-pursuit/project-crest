// service-worker.js

// Icon state management - using simple colored squares as fallback
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
    }
};

// Track active tabs for icon management
const activeTabs = new Set();

chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    if (details.url?.includes("youtube.com/watch")) {
        chrome.scripting.executeScript({
            target: { tabId: details.tabId },
            files: ["content-script-simple-working.js"]
        });
    }
});

chrome.runtime.onMessage.addListener((message, sender) => {
    // Handle real-time audio events
    if (message.type === 'AUDIO_LOUD_EVENT') {
        console.log('Crest: Audio loud event detected', message.data);

        fetch('http://localhost:5003/audio-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: 'audio_analysis',
                volume: message.data.volume,
                baseline: message.data.baseline,
                spike: message.data.spike,
                timestamp: message.data.timestamp
            }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.action === 'LOWER_VOLUME') {
                    setIconActive(sender.tab.id);
                    chrome.tabs.sendMessage(sender.tab.id, data);

                    const duration = data.duration || 3000;
                    setTimeout(() => {
                        setIconDefault(sender.tab.id);
                    }, duration + 500);

                    broadcastLogEvent(`🔊 Audio spike detected! Volume lowered to ${Math.round(data.level * 100)}%`);
                }
            })
            .catch(err => {
                console.error('Crest Audio Error:', err);
                broadcastLogEvent(`Audio Error: ${err.message}`);
            });
    }
    // Handle subtitle events (fallback)
    else if (message.type === 'SUBTITLE_DATA') {
        fetch('http://localhost:5003/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: message.text }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.action === 'LOWER_VOLUME') {
                    setIconActive(sender.tab.id);
                    chrome.tabs.sendMessage(sender.tab.id, data);

                    const duration = data.duration || 2000;
                    setTimeout(() => {
                        setIconDefault(sender.tab.id);
                    }, duration + 500);

                    broadcastLogEvent(`📝 Subtitle: Volume lowered to ${Math.round(data.level * 100)}% for ${duration}ms`);
                }
            })
            .catch(err => {
                console.error('Crest Error:', err);
                broadcastLogEvent(`Error: ${err.message}`);
            });
    }
    // Handle volume lowering from simple script
    else if (message.type === 'VOLUME_LOWERED') {
        console.log('Crest: Volume lowered by agent', message.data);

        setIconActive(sender.tab.id);

        const duration = message.data.duration || 3000;
        setTimeout(() => {
            setIconDefault(sender.tab.id);
        }, duration + 500);

        broadcastLogEvent(`🎵 Agent lowered volume to ${message.data.level}% for ${duration / 1000}s`);
    }
    // --- NEW: Handle user correction feedback ---
    else if (message.type === 'USER_CORRECTION') {
        fetch('http://localhost:5003/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event: 'user_corrected_volume' }),
        })
            .catch(err => console.error('Crest Feedback Error:', err));

        broadcastLogEvent('User corrected volume');
    }
    return true;
});

// Icon management functions
function setIconActive(tabId) {
    try {
        chrome.action.setIcon({
            path: IconState.ACTIVE,
            tabId: tabId
        });
        activeTabs.add(tabId);
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
        activeTabs.delete(tabId);
    } catch (error) {
        console.error('Error setting default icon:', error);
    }
}

// Clean up when tabs are closed
chrome.tabs.onRemoved.addListener((tabId) => {
    activeTabs.delete(tabId);
});

// Broadcast log events to popup
function broadcastLogEvent(text) {
    chrome.runtime.sendMessage({
        type: 'LOG_EVENT',
        text: text
    }).catch(() => {
        // Popup might not be open, ignore error
    });
}