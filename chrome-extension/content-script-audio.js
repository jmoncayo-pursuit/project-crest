// content-script-audio.js - Enhanced version with real audio analysis
console.log("Crest Audio Agent: Script Injected.");

let isAgentAdjusting = false;
let notification = null;
let notificationSettings = { enabled: true, volumeLevel: 0.3 };
let audioContext = null;
let analyser = null;
let audioSource = null;
let isMonitoring = false;

// Audio analysis parameters
const LOUD_THRESHOLD = 0.3; // Volume threshold for loud events (0-1) - lowered for better detection
const ANALYSIS_INTERVAL = 100; // Check audio every 100ms
const VOLUME_REDUCTION_DURATION = 3000; // 3 seconds
let lastLoudEventTime = 0;
let baselineVolume = 0.1; // Track normal volume levels - start lower

// --- ENHANCED: Real-time audio monitoring ---
function initializeAudioMonitoring() {
    const video = document.querySelector('video');
    if (!video) {
        console.log("Crest Audio Agent: No video found, retrying...");
        setTimeout(initializeAudioMonitoring, 1000);
        return;
    }

    // Wait for user interaction to start audio context (Chrome requirement)
    const startAudioContext = () => {
        try {
            console.log("Crest Audio Agent: Starting audio context...");

            // Create audio context
            audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Create analyser node
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 512; // Increased for better frequency resolution
            analyser.smoothingTimeConstant = 0.8;

            // Connect video to analyser
            audioSource = audioContext.createMediaElementSource(video);
            audioSource.connect(analyser);
            analyser.connect(audioContext.destination);

            console.log("Crest Audio Agent: Audio monitoring initialized successfully");

            // Start monitoring
            startAudioAnalysis();
            isMonitoring = true;

            // Remove event listeners after successful initialization
            video.removeEventListener('play', startAudioContext);
            video.removeEventListener('click', startAudioContext);
            document.removeEventListener('click', startAudioContext);

        } catch (error) {
            console.error("Crest Audio Agent: Failed to initialize audio monitoring:", error);
            // Fallback to subtitle-based monitoring
            initializeSubtitleMonitoring();
        }
    };

    // Try to start immediately (might work if user already interacted)
    if (audioContext === null) {
        // Add event listeners for user interaction
        video.addEventListener('play', startAudioContext, { once: true });
        video.addEventListener('click', startAudioContext, { once: true });
        document.addEventListener('click', startAudioContext, { once: true });

        console.log("Crest Audio Agent: Waiting for user interaction to start audio monitoring...");

        // Also try to start immediately in case video is already playing
        if (!video.paused) {
            startAudioContext();
        }
    }
}

function startAudioAnalysis() {
    if (!analyser || !isMonitoring) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function analyze() {
        if (!isMonitoring) return;

        analyser.getByteFrequencyData(dataArray);

        // Calculate current volume level
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            sum += dataArray[i];
        }
        const averageVolume = sum / bufferLength / 255; // Normalize to 0-1

        // Update baseline (moving average)
        baselineVolume = baselineVolume * 0.95 + averageVolume * 0.05;

        // Detect sudden loud events
        const volumeSpike = averageVolume - baselineVolume;
        const now = Date.now();

        // Log audio levels for debugging (every 2 seconds)
        if (now % 2000 < ANALYSIS_INTERVAL) {
            console.log(`Crest Audio Agent: Audio levels - Volume: ${averageVolume.toFixed(3)}, Baseline: ${baselineVolume.toFixed(3)}, Spike: ${volumeSpike.toFixed(3)}`);
        }

        // More sensitive detection with multiple conditions
        const isLoudEvent = (
            (volumeSpike > LOUD_THRESHOLD) || // Spike above threshold
            (averageVolume > 0.6 && volumeSpike > 0.15) || // High volume with medium spike
            (averageVolume > 0.8) // Very high absolute volume
        );

        if (isLoudEvent && (now - lastLoudEventTime) > 1500) { // Reduced cooldown
            console.log(`🔊 Crest Audio Agent: LOUD EVENT DETECTED! Volume: ${averageVolume.toFixed(3)}, Baseline: ${baselineVolume.toFixed(3)}, Spike: ${volumeSpike.toFixed(3)}`);

            // Send to AI for confirmation
            const audioData = {
                volume: averageVolume,
                baseline: baselineVolume,
                spike: volumeSpike,
                timestamp: now
            };

            chrome.runtime.sendMessage({
                type: 'AUDIO_LOUD_EVENT',
                data: audioData
            });

            lastLoudEventTime = now;
        }

        // Continue monitoring
        setTimeout(analyze, ANALYSIS_INTERVAL);
    }

    analyze();
}

// --- FALLBACK: Subtitle monitoring (original approach) ---
function initializeSubtitleMonitoring() {
    console.log("Crest Audio Agent: Using subtitle fallback mode");

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && node.classList.contains('ytp-caption-segment')) {
                    chrome.runtime.sendMessage({
                        type: 'SUBTITLE_DATA',
                        text: node.textContent
                    });
                }
            });
        });
    });

    function startObserver() {
        const captionWindow = document.querySelector('.ytp-caption-window-container');
        if (captionWindow) {
            observer.observe(captionWindow, { childList: true, subtree: true });
            console.log("Crest Audio Agent: Subtitle observer attached");
        } else {
            setTimeout(startObserver, 500);
        }
    }

    startObserver();
}

// --- Initialize notification system ---
function initializeNotification() {
    notification = document.createElement('div');
    notification.id = 'crest-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    `;
    document.body.appendChild(notification);
    console.log("Crest Audio Agent: Notification system initialized");
}

// Load user settings
function loadSettings() {
    chrome.storage.sync.get(['enableNotifications', 'volumeLevel'], (result) => {
        if (result.enableNotifications !== undefined) {
            notificationSettings.enabled = result.enableNotifications;
        }
        if (result.volumeLevel !== undefined) {
            notificationSettings.volumeLevel = result.volumeLevel;
        }
        console.log("Crest Audio Agent: Settings loaded:", notificationSettings);
    });
}

// --- ACTUATOR: Control the volume ---
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'LOWER_VOLUME') {
        const video = document.querySelector('video');
        if (video) {
            isAgentAdjusting = true;
            const originalVolume = video.volume;
            const targetLevel = notificationSettings.volumeLevel || message.level;

            console.log(`Crest Audio Agent: Lowering volume from ${originalVolume} to ${targetLevel} for ${message.duration}ms`);

            video.volume = targetLevel;

            // Show notification
            if (notificationSettings.enabled && notification) {
                showNotification(`🔉 Crest: Volume Lowered to ${Math.round(targetLevel * 100)}%`);
            }

            setTimeout(() => {
                video.volume = originalVolume;
                console.log(`Crest Audio Agent: Volume restored to ${originalVolume}`);

                if (notification) {
                    hideNotification();
                }

                setTimeout(() => { isAgentAdjusting = false; }, 100);
            }, message.duration);
        }
    }
    else if (message.type === 'SETTINGS_UPDATE') {
        notificationSettings = { ...notificationSettings, ...message.settings };
        console.log("Crest Audio Agent: Settings updated:", notificationSettings);
    }
});

// Notification management
function showNotification(text) {
    if (!notification) return;
    notification.textContent = text;
    notification.style.opacity = '1';
}

function hideNotification() {
    if (!notification) return;
    notification.style.opacity = '0';
}

// --- USER FEEDBACK: Detect manual volume changes ---
function addVolumeListener() {
    const video = document.querySelector('video');
    if (video) {
        video.addEventListener('volumechange', () => {
            if (!isAgentAdjusting) {
                console.log("Crest Audio Agent: User correction detected");
                chrome.runtime.sendMessage({ type: 'USER_CORRECTION' });
            }
        });
    } else {
        setTimeout(addVolumeListener, 500);
    }
}

// --- INITIALIZATION ---
function initialize() {
    console.log("Crest Audio Agent: Initializing...");

    initializeNotification();
    loadSettings();
    addVolumeListener();

    // Try audio monitoring first, fallback to subtitles
    setTimeout(() => {
        initializeAudioMonitoring();
    }, 1000);
}

// Start when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

// Handle page navigation (YouTube SPA)
let currentUrl = location.href;
new MutationObserver(() => {
    if (location.href !== currentUrl) {
        currentUrl = location.href;
        console.log("Crest Audio Agent: Page navigation detected, reinitializing...");

        // Stop current monitoring
        isMonitoring = false;

        // Reinitialize after navigation
        setTimeout(initialize, 2000);
    }
}).observe(document, { subtree: true, childList: true });