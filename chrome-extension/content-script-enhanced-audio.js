// content-script-enhanced-audio.js - Enhanced with real-time audio monitoring
console.log("🚀 Crest AI Agent: Enhanced Audio Script Injected and Ready!");

let isAgentAdjusting = false;
let notification = null;
let audioLevelMonitor = null;
let volumeController = null;

// --- AUDIO LEVEL MONITOR CLASS ---
class AudioLevelMonitor {
    constructor() {
        this.audioContext = null;
        this.analyser = null;
        this.source = null;
        this.baseline = 0.1;
        this.spikeThreshold = 0.3;
        this.isMonitoring = false;
        this.baselineHistory = [];
        this.maxBaselineHistory = 50; // Keep last 50 readings for baseline
        this.analysisInterval = null;
        this.lastSpikeTime = 0;
        this.spikeDebounce = 1000; // 1 second debounce between spikes
    }

    async startMonitoring(videoElement) {
        try {
            console.log("🎵 Crest: Starting audio level monitoring...");

            // Create audio context
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Handle suspended context (autoplay policy)
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }

            // Create analyser
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.analyser.smoothingTimeConstant = 0.8;

            // Connect video to analyser
            this.source = this.audioContext.createMediaElementSource(videoElement);
            this.source.connect(this.analyser);
            this.analyser.connect(this.audioContext.destination);

            // Start analysis loop (10Hz to prevent performance issues)
            this.analysisInterval = setInterval(() => {
                this.analyzeAudioLevel();
            }, 100);

            this.isMonitoring = true;
            console.log("✅ Crest: Audio monitoring started successfully");

        } catch (error) {
            console.error("❌ Crest: Failed to start audio monitoring:", error);
            // Fallback to subtitle-only mode
            this.isMonitoring = false;
        }
    }

    analyzeAudioLevel() {
        if (!this.analyser || !this.isMonitoring) return;

        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        this.analyser.getByteFrequencyData(dataArray);

        // Calculate RMS (Root Mean Square) for volume level
        const rms = this.calculateRMS(dataArray);

        // Update baseline with rolling average
        this.updateBaseline(rms);

        // Detect volume spikes
        const spike = rms - this.baseline;

        if (spike > this.spikeThreshold && this.shouldProcessSpike()) {
            console.log(`🔊 Crest: Audio spike detected! RMS: ${rms.toFixed(3)}, Baseline: ${this.baseline.toFixed(3)}, Spike: ${spike.toFixed(3)}`);
            this.sendAudioData(rms, this.baseline, spike);
            this.lastSpikeTime = Date.now();
        }
    }

    calculateRMS(dataArray) {
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
            const normalized = dataArray[i] / 255.0;
            sum += normalized * normalized;
        }
        return Math.sqrt(sum / dataArray.length);
    }

    updateBaseline(currentLevel) {
        this.baselineHistory.push(currentLevel);

        // Keep only recent history
        if (this.baselineHistory.length > this.maxBaselineHistory) {
            this.baselineHistory.shift();
        }

        // Calculate baseline as median of recent history (more robust than mean)
        const sorted = [...this.baselineHistory].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        this.baseline = sorted.length % 2 === 0
            ? (sorted[mid - 1] + sorted[mid]) / 2
            : sorted[mid];
    }

    shouldProcessSpike() {
        // Debounce spikes to prevent rapid-fire detections
        return (Date.now() - this.lastSpikeTime) > this.spikeDebounce;
    }

    sendAudioData(volume, baseline, spike) {
        chrome.runtime.sendMessage({
            type: 'AUDIO_DATA',
            data: {
                volume: volume,
                baseline: baseline,
                spike: spike,
                timestamp: Date.now()
            }
        });
    }

    stop() {
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
            this.analysisInterval = null;
        }

        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }

        this.isMonitoring = false;
        console.log("🔇 Crest: Audio monitoring stopped");
    }
}

// --- ENHANCED VOLUME CONTROLLER CLASS ---
class VolumeController {
    constructor() {
        this.isAdjusting = false;
        this.currentReduction = 0;
        this.transitionDuration = 500;
        this.originalVolume = 1.0;
        this.activeAdjustments = new Set();
    }

    async applyVolumeReduction(level, duration, confidence, trigger = 'unknown') {
        const video = document.querySelector('video');
        if (!video) {
            console.log("❌ Crest: No video element found for volume control");
            return;
        }

        // Create unique adjustment ID
        const adjustmentId = `${trigger}_${Date.now()}`;
        this.activeAdjustments.add(adjustmentId);

        // Store original volume if not already adjusting
        if (!this.isAdjusting) {
            this.originalVolume = video.volume;
        }

        this.isAdjusting = true;

        // Apply confidence-based adjustment
        const confidenceMultiplier = confidence >= 0.8 ? 1.0 : 0.5;
        const targetLevel = level * confidenceMultiplier;

        console.log(`🔉 Crest: Applying volume reduction (${trigger})`);
        console.log(`   Original: ${this.originalVolume.toFixed(3)}, Target: ${targetLevel.toFixed(3)}, Confidence: ${confidence.toFixed(2)}`);

        // Smooth volume transition
        await this.smoothVolumeTransition(video, video.volume, targetLevel, 200);

        // Show notification
        if (notification) {
            const confidenceText = confidence >= 0.8 ? 'High' : 'Medium';
            showNotification(`🔉 Crest AI: Volume lowered (${confidenceText} confidence, ${trigger})`);
        }

        // Restore volume after duration
        setTimeout(async () => {
            this.activeAdjustments.delete(adjustmentId);

            // Only restore if no other adjustments are active
            if (this.activeAdjustments.size === 0) {
                console.log(`🔊 Crest: Restoring volume to ${this.originalVolume.toFixed(3)}`);
                await this.smoothVolumeTransition(video, video.volume, this.originalVolume, this.transitionDuration);

                if (notification) {
                    hideNotification();
                }

                setTimeout(() => {
                    this.isAdjusting = false;
                    this.currentReduction = 0;
                }, 100);
            }
        }, duration);
    }

    async smoothVolumeTransition(video, startVolume, endVolume, duration) {
        return new Promise((resolve) => {
            const startTime = Date.now();
            const volumeDiff = endVolume - startVolume;

            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Use easeInOutQuad for smooth transition
                const easeProgress = progress < 0.5
                    ? 2 * progress * progress
                    : 1 - Math.pow(-2 * progress + 2, 2) / 2;

                video.volume = startVolume + (volumeDiff * easeProgress);

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    video.volume = endVolume;
                    resolve();
                }
            };

            animate();
        });
    }
}

// --- Initialize notification system ---
function initializeNotification() {
    notification = document.createElement('div');
    notification.id = 'crest-notification';
    notification.style.cssText = `
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
    document.body.appendChild(notification);
    console.log("✅ Crest: Enhanced notification system initialized");
}

// --- SUBTITLE MONITORING (Existing functionality) ---
function initializeSubtitleMonitoring() {
    console.log("🔍 Crest: Starting subtitle monitoring...");

    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1 && node.classList.contains('ytp-caption-segment')) {
                    const subtitleText = node.textContent;
                    console.log("📝 Crest: Subtitle detected:", subtitleText);

                    // Send to AI for analysis
                    chrome.runtime.sendMessage({
                        type: 'SUBTITLE_DATA',
                        text: subtitleText
                    });
                }
            });
        });
    });

    function startObserver() {
        const captionWindow = document.querySelector('.ytp-caption-window-container');
        if (captionWindow) {
            observer.observe(captionWindow, { childList: true, subtree: true });
            console.log("✅ Crest: Subtitle observer attached");
        } else {
            console.log("⏳ Crest: Waiting for captions...");
            setTimeout(startObserver, 1000);
        }
    }

    startObserver();
}

// --- DUAL DETECTION COORDINATION ---
class DetectionCoordinator {
    constructor() {
        this.recentDetections = new Map();
        this.coordinationWindow = 2000; // 2 second window for coordination
    }

    shouldProcessDetection(trigger, confidence) {
        const now = Date.now();

        // Check for recent detections from other triggers
        for (const [otherTrigger, detection] of this.recentDetections) {
            if (otherTrigger !== trigger && (now - detection.timestamp) < this.coordinationWindow) {
                console.log(`🔄 Crest: Coordinating ${trigger} detection with recent ${otherTrigger} detection`);

                // If we have a higher confidence detection, proceed
                if (confidence > detection.confidence + 0.1) {
                    console.log(`✅ Crest: ${trigger} has higher confidence (${confidence.toFixed(2)} vs ${detection.confidence.toFixed(2)})`);
                    this.recentDetections.set(trigger, { timestamp: now, confidence });
                    return true;
                }

                // Otherwise, skip to avoid duplicate adjustment
                console.log(`⏭️ Crest: Skipping ${trigger} detection due to recent ${otherTrigger} detection`);
                return false;
            }
        }

        // No recent detections, proceed
        this.recentDetections.set(trigger, { timestamp: now, confidence });
        this.cleanupOldDetections();
        return true;
    }

    cleanupOldDetections() {
        const now = Date.now();
        for (const [trigger, detection] of this.recentDetections) {
            if (now - detection.timestamp > this.coordinationWindow) {
                this.recentDetections.delete(trigger);
            }
        }
    }
}

const detectionCoordinator = new DetectionCoordinator();

// --- ENHANCED MESSAGE HANDLING ---
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'LOWER_VOLUME') {
        const confidence = message.confidence || 0.8;
        const trigger = message.trigger || 'subtitle';

        // Coordinate with other detection methods
        if (!detectionCoordinator.shouldProcessDetection(trigger, confidence)) {
            console.log(`🚫 Crest: Skipping ${trigger} volume adjustment due to coordination`);
            return;
        }

        if (volumeController) {
            volumeController.applyVolumeReduction(
                message.level || 0.3,
                message.duration || 3000,
                confidence,
                trigger
            );
        }
    } else if (message.action === 'TEST_AUDIO_MONITORING') {
        // Handle test request from popup
        testAudioMonitoring();
    }
});

// --- NOTIFICATION MANAGEMENT ---
function showNotification(text) {
    if (!notification) return;
    notification.textContent = text;
    notification.style.opacity = '1';
    console.log("📢 Crest:", text);
}

function hideNotification() {
    if (!notification) return;
    notification.style.opacity = '0';
}

// --- USER FEEDBACK DETECTION ---
function addVolumeListener() {
    const video = document.querySelector('video');
    if (video) {
        video.addEventListener('volumechange', () => {
            if (!volumeController?.isAdjusting) {
                console.log("👤 Crest: User manually adjusted volume");
                chrome.runtime.sendMessage({ type: 'USER_CORRECTION' });
            }
        });
        console.log("✅ Crest: Volume change listener added");
    } else {
        setTimeout(addVolumeListener, 1000);
    }
}

// --- ENHANCED TESTING FUNCTIONS ---
function testVolumeControl() {
    console.log("🧪 Crest: Running enhanced volume test...");
    if (volumeController) {
        volumeController.applyVolumeReduction(0.2, 2000, 0.9, 'manual_test');
    }
}

function testAudioMonitoring() {
    console.log("🧪 Crest: Testing audio monitoring...");
    if (audioLevelMonitor && audioLevelMonitor.isMonitoring) {
        console.log(`   Baseline: ${audioLevelMonitor.baseline.toFixed(3)}`);
        console.log(`   Threshold: ${audioLevelMonitor.spikeThreshold.toFixed(3)}`);
        console.log("   Monitoring: Active");
    } else {
        console.log("   Monitoring: Inactive");
    }
}

// Make test functions globally available
window.testCrestVolumeControl = testVolumeControl;
window.testCrestAudioMonitoring = testAudioMonitoring;

// --- ENHANCED INITIALIZATION ---
async function initialize() {
    console.log("🚀 Crest: Initializing enhanced AI-powered volume control...");

    const video = document.querySelector('video');
    if (video) {
        console.log("✅ Crest: Video element found, volume:", video.volume.toFixed(3));

        // Initialize components
        volumeController = new VolumeController();
        audioLevelMonitor = new AudioLevelMonitor();

        // Start audio monitoring
        try {
            await audioLevelMonitor.startMonitoring(video);
        } catch (error) {
            console.warn("⚠️ Crest: Audio monitoring failed, continuing with subtitle-only mode");
        }

    } else {
        console.log("⏳ Crest: Waiting for video element...");
    }

    initializeNotification();
    addVolumeListener();
    initializeSubtitleMonitoring();

    console.log("✅ Crest: Enhanced initialization complete!");
    console.log("💡 Crest: Test commands:");
    console.log("   - testCrestVolumeControl() - Test volume control");
    console.log("   - testCrestAudioMonitoring() - Check audio monitoring status");
}

// --- CLEANUP ON PAGE UNLOAD ---
window.addEventListener('beforeunload', () => {
    if (audioLevelMonitor) {
        audioLevelMonitor.stop();
    }
});

// Start initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

// Handle YouTube SPA navigation
let currentUrl = location.href;
new MutationObserver(() => {
    if (location.href !== currentUrl) {
        currentUrl = location.href;
        console.log("🔄 Crest: Page navigation detected, reinitializing...");

        // Cleanup existing monitoring
        if (audioLevelMonitor) {
            audioLevelMonitor.stop();
        }

        // Reinitialize after delay
        setTimeout(initialize, 2000);
    }
}).observe(document, { subtree: true, childList: true });