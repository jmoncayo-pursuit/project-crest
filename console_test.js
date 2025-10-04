// CREST EXTENSION CONSOLE TEST
// Copy and paste this entire script into YouTube console

console.log("🚀 STARTING CREST EXTENSION TEST");
console.log("================================");

// Test 1: Check if extension is loaded
console.log("1. Checking extension status...");
const video = document.querySelector('video');
const notification = document.getElementById('crest-notification');

console.log("✅ Video element found:", !!video);
console.log("✅ Notification element found:", !!notification);

if (!video) {
    console.error("❌ No video element found! Make sure you're on a YouTube video page.");
} else {
    console.log("📹 Video info:", {
        paused: video.paused,
        volume: video.volume,
        duration: video.duration
    });
}

// Test 2: Force user interaction for audio context
console.log("\n2. Triggering user interaction...");
if (video && video.paused) {
    video.play();
    console.log("▶️ Started video playback");
}

// Test 3: Wait and check audio monitoring
setTimeout(() => {
    console.log("\n3. Checking audio monitoring status...");

    // Test 4: Send manual loud event
    console.log("\n4. Sending manual loud event...");
    try {
        chrome.runtime.sendMessage({
            type: 'AUDIO_LOUD_EVENT',
            data: {
                volume: 0.85,
                baseline: 0.2,
                spike: 0.65,
                timestamp: Date.now()
            }
        });
        console.log("✅ Manual loud event sent to service worker");

        // Test 5: Check for volume change
        setTimeout(() => {
            console.log("\n5. Checking if volume changed...");
            console.log("Current video volume:", video.volume);

            if (video.volume < 0.5) {
                console.log("🎉 SUCCESS! Volume was lowered by the agent!");
            } else {
                console.log("⚠️ Volume not changed. Check service worker console for errors.");
            }
        }, 2000);

    } catch (error) {
        console.error("❌ Failed to send message:", error);
        console.log("💡 Try reloading the extension at chrome://extensions/");
    }
}, 3000);

// Test 6: Manual volume test
console.log("\n6. Running manual volume test in 8 seconds...");
setTimeout(() => {
    if (video) {
        const originalVolume = video.volume;
        console.log("📊 Testing manual volume control...");
        console.log("Original volume:", originalVolume);

        video.volume = 0.2;
        console.log("Volume set to:", video.volume);

        setTimeout(() => {
            video.volume = originalVolume;
            console.log("Volume restored to:", originalVolume);
            console.log("\n🏁 TEST COMPLETE!");
            console.log("If you saw volume changes, the extension is working!");
        }, 3000);
    }
}, 8000);

console.log("\n⏱️ Test will run for ~12 seconds. Watch the console output...");