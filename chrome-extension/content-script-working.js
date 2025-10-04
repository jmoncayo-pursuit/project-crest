// content-script-working.js - Complete AI-powered version
console.log("🚀 Crest AI Agent: Script Injected and Ready!");

let isAgentAdjusting = false;
let notification = null;
let notificationSettings = { enabled: true, volumeLevel: 0.3 };

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
    console.log("✅ Crest: Notification system initialized");
}

// --- SUBTITLE MONITORING (Primary approach) ---
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

// --- VOLUME CONTROL (Core functionality) ---
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === 'LOWER_VOLUME') {
        const video = document.querySelector('video');
        if (video) {
            isAgentAdjusting = true;
            const originalVolume = video.volume;
            const targetLevel = message.level || 0.3;
            const duration = message.duration || 3000;

            console.log(`🔉 Crest: Lowering volume from ${originalVolume.toFixed(2)} to ${targetLevel.toFixed(2)} for ${duration}ms`);

            // Apply volume reduction
            video.volume = targetLevel;

            // Show notification
            if (notification) {
                showNotification(`🔉 Crest AI: Volume lowered to ${Math.round(targetLevel * 100)}%`);
            }

            // Restore volume after duration
            setTimeout(() => {
                video.volume = originalVolume;
                console.log(`🔊 Crest: Volume restored to ${originalVolume.toFixed(2)}`);

                if (notification) {
                    hideNotification();
                }

                setTimeout(() => { isAgentAdjusting = false; }, 100);
            }, duration);
        } else {
            console.log("❌ Crest: No video element found");
        }
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
            if (!isAgentAdjusting) {
                console.log("👤 Crest: User manually adjusted volume");
                chrome.runtime.sendMessage({ type: 'USER_CORRECTION' });
            }
        });
        console.log("✅ Crest: Volume change listener added");
    } else {
        setTimeout(addVolumeListener, 1000);
    }
}

// --- MANUAL TESTING FUNCTIONS ---
function testVolumeControl() {
    console.log("🧪 Crest: Running manual volume test...");
    const video = document.querySelector('video');
    if (video) {
        const originalVolume = video.volume;
        video.volume = 0.2;
        showNotification("🧪 Manual Test: Volume lowered to 20%");

        setTimeout(() => {
            video.volume = originalVolume;
            hideNotification();
            console.log("✅ Crest: Manual test completed");
        }, 2000);
    }
}

// Make test function globally available
window.testCrestVolumeControl = testVolumeControl;

// --- INITIALIZATION ---
function initialize() {
    console.log("🚀 Crest: Initializing AI-powered volume control...");

    const video = document.querySelector('video');
    if (video) {
        console.log("✅ Crest: Video element found, volume:", video.volume.toFixed(3));
    } else {
        console.log("⏳ Crest: Waiting for video element...");
    }

    initializeNotification();
    addVolumeListener();
    initializeSubtitleMonitoring();

    console.log("✅ Crest: Initialization complete!");
    console.log("💡 Crest: To test manually, run: testCrestVolumeControl()");
}

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
        setTimeout(initialize, 2000);
    }
}).observe(document, { subtree: true, childList: true });