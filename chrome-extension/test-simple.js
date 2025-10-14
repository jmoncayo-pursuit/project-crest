// Super simple test script
console.log("🚀 CREST TEST: Script loaded successfully!");

// Show a visible notification
const notification = document.createElement('div');
notification.textContent = '🎵 CREST LOADED - Check console for more info';
notification.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: red;
    color: white;
    padding: 10px;
    z-index: 999999;
    border-radius: 5px;
    font-weight: bold;
`;
document.body.appendChild(notification);

// Test volume control after 5 seconds
setTimeout(() => {
    const video = document.querySelector('video');
    if (video) {
        console.log("🎵 CREST: Found video, testing volume control...");
        const originalVolume = video.volume;
        video.volume = 0.2;

        notification.textContent = '🎵 CREST: Volume lowered to 20%';
        notification.style.background = 'green';

        setTimeout(() => {
            video.volume = originalVolume;
            notification.textContent = '🎵 CREST: Volume restored';
            console.log("🎵 CREST: Volume restored");
        }, 3000);
    } else {
        console.log("❌ CREST: No video found");
        notification.textContent = '❌ CREST: No video found';
    }
}, 5000);

console.log("🎵 CREST: Test script setup complete - will test volume in 5 seconds");