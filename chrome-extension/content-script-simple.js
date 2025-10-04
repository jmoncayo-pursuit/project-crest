// Simple test content script
console.log("🚀 SIMPLE CREST TEST: Script loaded successfully!");

// Test basic functionality
const video = document.querySelector('video');
if (video) {
    console.log("✅ Video found, volume:", video.volume);

    // Add a simple volume test
    setTimeout(() => {
        const originalVolume = video.volume;
        video.volume = 0.3;
        console.log("🔉 Volume lowered to 30%");

        setTimeout(() => {
            video.volume = originalVolume;
            console.log("🔊 Volume restored");
        }, 2000);
    }, 3000);
} else {
    console.log("❌ No video found");
}

// Test chrome.runtime
if (chrome && chrome.runtime) {
    console.log("✅ Chrome runtime available");
} else {
    console.log("❌ Chrome runtime not available");
}