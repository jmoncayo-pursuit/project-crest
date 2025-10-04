// Enhanced Content Script - Handles both audio analysis and subtitles
console.log("🚀 Crest Enhanced Agent: Loading...");

class CrestAgent {
    constructor() {
        this.isActive = false;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.baselineVolume = 0;
        this.volumeHistory = [];
        this.lastVolumeAdjustment = 0;
        this.isAdjusting = false;

        // Notification system
        this.notification = null;
        this.initNotification();

        // Initialize both monitoring systems
        this.initAudioMonitoring();
        this.initSubtitleMonitoring();
        this.initVolumeListener();

        console.log("✅ Crest Enhanced Agent: Ready!");
    }

    initNotification() {
        this.notification = document.createElement('div');
        this.notification.id = 'crest-notification';
        this.notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 12px 18px;
            border-radius: 8px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            border: 2px solid #ff6b35;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        document.body.appendChild(this.notification);
    }

    showNotification(text, duration = 3000) {
        if (!this.notification) return;
        this.notification.textContent = text;
        this.notification.style.opacity = '1';

        setTimeout(() => {
            this.notification.style.opacity = '0';
        }, duration);
    }

    async initAudioMonitoring() {
        try {
            const video = document.querySelector('video');
            if (!video) {
                setTimeout(() => this.initAudioMonitoring(), 1000);
                return;
            }

            // Create audio context
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = this.audioContext.createMediaElementSource(video);
            this.analyser = this.audioContext.createAnalyser();

            // Connect audio nodes
            source.connect(this.analyser);
            this.analyser.connect(this.audioContext.destination);

            // Configure analyser
            this.analyser.fftSize = 256;
            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);

            console.log("✅ Crest: Audio monitoring initialized");
            this.startAudioAnalysis();

        } catch (error) {
            console.log("⚠️ Crest: Audio monitoring failed, using subtitle-only mode");
            console.error(error);
        }
    }

    startAudioAnalysis() {
        const analyzeAudio = () => {
            if (!this.analyser || !this.dataArray) return;

            this.analyser.getByteFrequencyData(this.dataArray);

            // Calculate current volume level
            const sum = this.dataArray.reduce((a, b) => a + b, 0);
            const currentVolume = sum / this.dataArray.length / 255;

            // Update volume history
            this.volumeHistory.push(currentVolume);
            if (this.volumeHistory.length > 30) { // Keep last 30 samples (~1 second)
                this.volumeHistory.shift();
            }

            // Calculate baseline (average of recent history)
            if (this.volumeHistory.length >= 10) {
                this.baselineVolume = this.volumeHistory.reduce((a, b) => a + b, 0) / this.volumeHistory.length;

                // Detect volume spikes
                const spike = currentVolume - this.baselineVolume;

                // Only trigger if significant spike and not recently adjusted
                if (spike > 0.3 && currentVolume > 0.4 && !this.isAdjusting &&
                    Date.now() - this.lastVolumeAdjustment > 2000) {

                    console.log(`🔊 Crest: Audio spike detected! Current: ${currentVolume.toFixed(3)}, Baseline: ${this.baselineVolume.toFixed(3)}, Spike: ${spike.toFixed(3)}`);

                    // Send to AI for analysis
                    chrome.runtime.sendMessage({
                        type: 'AUDIO_LOUD_EVENT',
                        data: {
                            volume: currentVolume,
                            baseline: this.baselineVolume,
                            spike: spike,
                            timestamp: Date.now()
                        }
                    });
                }
            }

            requestAnimationFrame(analyzeAudio);
        };

        analyzeAudio();
    }

    initSubtitleMonitoring() {
        console.log("🔍 Crest: Starting subtitle monitoring...");

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList.contains('ytp-caption-segment')) {
                        const subtitleText = node.textContent;
                        if (subtitleText && subtitleText.trim()) {
                            console.log("📝 Crest: Subtitle detected:", subtitleText);

                            // Send to AI for analysis
                            chrome.runtime.sendMessage({
                                type: 'SUBTITLE_DATA',
                                text: subtitleText
                            });
                        }
                    }
                });
            });
        });

        const startObserver = () => {
            const captionWindow = document.querySelector('.ytp-caption-window-container');
            if (captionWindow) {
                observer.observe(captionWindow, { childList: true, subtree: true });
                console.log("✅ Crest: Subtitle observer attached");
            } else {
                setTimeout(startObserver, 1000);
            }
        };

        startObserver();
    }

    initVolumeListener() {
        const video = document.querySelector('video');
        if (video) {
            video.addEventListener('volumechange', () => {
                if (!this.isAdjusting) {
                    console.log("👤 Crest: User manually adjusted volume");
                    chrome.runtime.sendMessage({ type: 'USER_CORRECTION' });
                }
            });
            console.log("✅ Crest: Volume change listener added");
        } else {
            setTimeout(() => this.initVolumeListener(), 1000);
        }
    }
}

// Listen for volume control messages from service worker
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'LOWER_VOLUME') {
        const video = document.querySelector('video');
        if (video) {
            const agent = window.crestAgent;
            if (agent) {
                agent.isAdjusting = true;
                agent.lastVolumeAdjustment = Date.now();
            }

            const originalVolume = video.volume;
            const targetLevel = message.level || 0.3;
            const duration = message.duration || 3000;

            console.log(`🔉 Crest: Lowering volume from ${originalVolume.toFixed(2)} to ${targetLevel.toFixed(2)} for ${duration}ms`);

            // Apply volume reduction
            video.volume = targetLevel;

            // Show notification
            if (window.crestAgent && window.crestAgent.notification) {
                window.crestAgent.showNotification(`🔉 Crest AI: Volume lowered to ${Math.round(targetLevel * 100)}%`, duration);
            }

            // Restore volume after duration
            setTimeout(() => {
                video.volume = originalVolume;
                console.log(`🔊 Crest: Volume restored to ${originalVolume.toFixed(2)}`);

                if (agent) {
                    setTimeout(() => { agent.isAdjusting = false; }, 100);
                }
            }, duration);
        }
    }
});

// Initialize agent when ready
function initializeCrestAgent() {
    const video = document.querySelector('video');
    if (video && !window.crestAgent) {
        window.crestAgent = new CrestAgent();

        // Make test function available
        window.testCrestVolumeControl = () => {
            const video = document.querySelector('video');
            if (video) {
                const originalVolume = video.volume;
                video.volume = 0.2;
                window.crestAgent.showNotification("🧪 Manual Test: Volume lowered to 20%", 2000);

                setTimeout(() => {
                    video.volume = originalVolume;
                    console.log("✅ Crest: Manual test completed");
                }, 2000);
            }
        };

        console.log("💡 Crest: To test manually, run: testCrestVolumeControl()");
    } else if (!video) {
        setTimeout(initializeCrestAgent, 1000);
    }
}

// Start initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCrestAgent);
} else {
    initializeCrestAgent();
}

// Handle YouTube SPA navigation
let currentUrl = location.href;
new MutationObserver(() => {
    if (location.href !== currentUrl) {
        currentUrl = location.href;
        console.log("🔄 Crest: Page navigation detected, reinitializing...");
        setTimeout(initializeCrestAgent, 2000);
    }
}).observe(document, { subtree: true, childList: true });