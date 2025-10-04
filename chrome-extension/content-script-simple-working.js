// SIMPLE WORKING CONTENT SCRIPT - Detects any audio and lowers volume
console.log("🎵 Crest Simple Agent: Script Loaded!");

let isMonitoring = false;
let lastVolumeChange = 0;

function startSimpleMonitoring() {
    const video = document.querySelector('video');
    if (!video) {
        console.log("❌ No video found, retrying...");
        setTimeout(startSimpleMonitoring, 1000);
        return;
    }

    console.log("✅ Video found, starting monitoring...");

    // Simple approach: monitor volume changes and audio events
    let audioContext;
    let analyser;
    let audioSource;

    // Wait for user interaction to create audio context
    const startAudioContext = () => {
        try {
            console.log("🎧 Creating audio context after user interaction...");
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            analyser.smoothingTimeConstant = 0.8;

            // Connect to video
            audioSource = audioContext.createMediaElementSource(video);
            audioSource.connect(analyser);
            analyser.connect(audioContext.destination);

            console.log("✅ Real audio analysis started!");
            startAudioAnalysis();

            // Remove event listeners after success
            video.removeEventListener('play', startAudioContext);
            video.removeEventListener('click', startAudioContext);
            document.removeEventListener('click', startAudioContext);

        } catch (error) {
            console.log("❌ Audio context still failed:", error);
            startFallbackMonitoring();
        }
    };

    // Add event listeners for user interaction
    video.addEventListener('play', startAudioContext, { once: true });
    video.addEventListener('click', startAudioContext, { once: true });
    document.addEventListener('click', startAudioContext, { once: true });

    console.log("⏳ Waiting for user interaction to start real audio analysis...");
    console.log("💡 Click play or anywhere on the page to activate!");

    // If video is already playing, try immediately
    if (!video.paused) {
        startAudioContext();
    }
}

function startAudioAnalysis() {
    console.log("🔊 Starting real-time audio analysis...");

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    let analysisCount = 0;

    function analyze() {
        if (!analyser) return;

        analyser.getByteFrequencyData(dataArray);

        // Calculate volume
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            sum += dataArray[i];
        }
        const volume = sum / bufferLength / 255;

        analysisCount++;

        // Log every 5 analyses (about every second)
        if (analysisCount % 5 === 0) {
            console.log(`🎵 REAL AUDIO: ${(volume * 100).toFixed(1)}%`);
        }

        // SUPER sensitive detection - any volume above 3%
        if (volume > 0.03) {
            const now = Date.now();
            if (now - lastVolumeChange > 2000) { // 2 second cooldown
                console.log(`🚨 REAL AUDIO SPIKE DETECTED! Volume: ${(volume * 100).toFixed(1)}% - LOWERING VOLUME`);
                lowerVolume();
                lastVolumeChange = now;
            }
        }

        // Continue monitoring
        setTimeout(analyze, 200); // Check every 200ms
    }

    analyze();
}

function startFallbackMonitoring() {
    console.log("📺 Using fallback monitoring (video events)...");

    const video = document.querySelector('video');
    if (!video) return;

    // Monitor video events
    video.addEventListener('play', () => {
        console.log("▶️ Video started playing - simulating audio detection");
        setTimeout(() => {
            console.log("🚨 SIMULATED AUDIO SPIKE - LOWERING VOLUME");
            lowerVolume();
        }, 2000);
    });

    // Also trigger on volume changes (user interaction)
    video.addEventListener('volumechange', () => {
        if (video.volume > 0.5) {
            console.log("🔊 High volume detected - simulating loud event");
            setTimeout(() => {
                lowerVolume();
            }, 1000);
        }
    });
}

function lowerVolume() {
    const video = document.querySelector('video');
    if (!video) return;

    const originalVolume = video.volume;
    const targetVolume = 0.25;
    const duration = 3000;

    console.log(`📉 Lowering volume from ${Math.round(originalVolume * 100)}% to ${Math.round(targetVolume * 100)}%`);

    // Notify service worker about volume change
    chrome.runtime.sendMessage({
        type: 'VOLUME_LOWERED',
        data: {
            originalVolume: Math.round(originalVolume * 100),
            targetVolume: Math.round(targetVolume * 100),
            level: Math.round(targetVolume * 100),
            duration: duration
        }
    });

    // Show notification
    showNotification(`🔉 Agent lowered volume to ${Math.round(targetVolume * 100)}%`);

    // Lower volume
    video.volume = targetVolume;

    // Restore after 3 seconds
    setTimeout(() => {
        video.volume = originalVolume;
        console.log(`📈 Volume restored to ${Math.round(originalVolume * 100)}%`);
        showNotification(`✅ Volume restored to ${Math.round(originalVolume * 100)}%`);
    }, duration);
}

function showNotification(message) {
    // Remove existing notification
    const existing = document.getElementById('crest-notification');
    if (existing) existing.remove();

    // Create notification
    const notification = document.createElement('div');
    notification.id = 'crest-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        z-index: 999999;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(notification);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        if (notification) notification.remove();
    }, 4000);
}

// Start monitoring when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startSimpleMonitoring);
} else {
    startSimpleMonitoring();
}

// Handle YouTube navigation
let currentUrl = location.href;
new MutationObserver(() => {
    if (location.href !== currentUrl) {
        currentUrl = location.href;
        console.log("🔄 Page navigation detected, restarting monitoring...");
        setTimeout(startSimpleMonitoring, 2000);
    }
}).observe(document, { subtree: true, childList: true });