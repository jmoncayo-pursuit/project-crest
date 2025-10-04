// SIMPLE TEST SCRIPT - Just logs to console every second
console.log("🚀 TEST SCRIPT LOADED!");

setInterval(() => {
    console.log("🎵 Test script is running - " + new Date().toLocaleTimeString());
}, 1000);

// Test if we can find video
const video = document.querySelector('video');
if (video) {
    console.log("✅ Video found:", video);
} else {
    console.log("❌ No video found");
}

// Test basic functionality
setTimeout(() => {
    console.log("🔧 Testing basic volume control...");
    const video = document.querySelector('video');
    if (video) {
        const originalVolume = video.volume;
        console.log("Original volume:", originalVolume);

        video.volume = 0.3;
        console.log("Volume set to:", video.volume);

        setTimeout(() => {
            video.volume = originalVolume;
            console.log("Volume restored to:", originalVolume);
        }, 2000);
    }
}, 3000);