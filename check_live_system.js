// PASTE THIS IN YOUTUBE CONSOLE TO CHECK IF EXTENSION IS WORKING
console.log("🔍 CHECKING CREST EXTENSION STATUS");

// Check 1: Video element
const video = document.querySelector('video');
console.log("✅ Video found:", !!video);

// Check 2: Extension content script loaded
console.log("🔍 Looking for Crest content script...");

// Check 3: Try to send message to service worker
if (typeof chrome !== 'undefined' && chrome.runtime) {
    console.log("✅ Chrome extension API available");

    // Test message to service worker
    chrome.runtime.sendMessage({
        type: 'SUBTITLE_DATA',
        text: '[explosion]'
    }, (response) => {
        if (chrome.runtime.lastError) {
            console.log("❌ Service worker error:", chrome.runtime.lastError.message);
        } else {
            console.log("✅ Service worker responded:", response);
        }
    });

} else {
    console.log("❌ Chrome extension API not available");
}

// Check 4: Test server connection directly
fetch('http://localhost:5003/health')
    .then(response => response.json())
    .then(data => {
        console.log("✅ Server connection working:", data);

        // Test AI endpoint
        return fetch('http://localhost:5003/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: '[explosion]' })
        });
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ AI endpoint working:", data);
        if (data.action === 'LOWER_VOLUME') {
            console.log("🎉 AI DETECTED LOUD EVENT - SYSTEM IS WORKING!");
        }
    })
    .catch(error => {
        console.log("❌ Server connection failed:", error);
        console.log("💡 Make sure server is running: python app.py");
    });

console.log("🔍 Check complete - look for results above");