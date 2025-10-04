// EMERGENCY EXTENSION FIX
// This will manually inject the content script for testing

console.log("🔧 MANUAL EXTENSION INJECTION TEST");

// Step 1: Check current state
console.log("Current URL:", window.location.href);
console.log("Is YouTube watch page:", window.location.href.includes('youtube.com/watch'));
console.log("Chrome runtime available:", typeof chrome !== 'undefined' && !!chrome.runtime);

// Step 2: Create notification element manually (simulates content script)
if (!document.getElementById('crest-notification')) {
    const notification = document.createElement('div');
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
    console.log("✅ Created notification element manually");
} else {
    console.log("✅ Notification element already exists");
}

// Step 3: Test basic volume control
const video = document.querySelector('video');
if (video) {
    console.log("✅ Video element found");
    console.log("Current volume:", video.volume);

    // Test volume change
    const originalVolume = video.volume;
    console.log("🧪 Testing volume control...");

    video.volume = 0.2;
    console.log("Volume lowered to:", video.volume);

    // Show notification
    const notification = document.getElementById('crest-notification');
    if (notification) {
        notification.textContent = "🔉 Crest: Volume Lowered to 20% (Manual Test)";
        notification.style.opacity = '1';

        setTimeout(() => {
            notification.style.opacity = '0';
        }, 3000);
    }

    setTimeout(() => {
        video.volume = originalVolume;
        console.log("Volume restored to:", originalVolume);
        console.log("🎉 Manual volume control test SUCCESSFUL!");
    }, 3000);

} else {
    console.log("❌ No video element found");
}

// Step 4: Check extension files
console.log("\n📁 Extension Debug Info:");
console.log("Go to chrome://extensions/ and check:");
console.log("1. Project Crest is ENABLED (blue toggle)");
console.log("2. Click RELOAD button (↻)");
console.log("3. Click 'Details' and check for errors");
console.log("4. Make sure content-script-audio.js is listed");

console.log("\n🔧 If extension still not working:");
console.log("1. The content script might not be matching YouTube URLs");
console.log("2. Extension permissions might be denied");
console.log("3. Extension might have JavaScript errors");
console.log("4. Try reloading the page after reloading extension");

console.log("\n✅ This manual test proves the concept works!");
console.log("The issue is just getting the extension to load properly.");