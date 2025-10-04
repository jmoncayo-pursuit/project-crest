// WORKING SUBTLE DEMO - Takes the working parts and makes them subtle
const video = document.querySelector('video');
console.log('Video found:', !!video);

if (video) {
    const originalVolume = video.volume;
    console.log('Current volume:', Math.round(video.volume * 100) + '%');

    // Create small notification in corner
    const overlay = document.createElement('div');
    overlay.textContent = '🎵 Crest AI: Monitoring';
    overlay.style.cssText = 'position:fixed;top:20px;right:20px;background:rgba(0,0,0,0.8);color:white;padding:10px 15px;font-size:14px;z-index:999999;border-radius:5px;border-left:3px solid #4CAF50;';
    document.body.appendChild(overlay);

    setTimeout(() => {
        overlay.textContent = '🚨 Loud event detected';
        overlay.style.borderLeftColor = '#FF9800';
    }, 1000);

    setTimeout(() => {
        video.volume = 0.2;
        overlay.textContent = '🔉 Volume lowered to ' + Math.round(video.volume * 100) + '%';
        overlay.style.borderLeftColor = '#F44336';
        console.log('Volume lowered to:', Math.round(video.volume * 100) + '%');
    }, 2000);

    setTimeout(() => {
        video.volume = originalVolume;
        overlay.textContent = '✅ Volume restored to ' + Math.round(video.volume * 100) + '%';
        overlay.style.borderLeftColor = '#4CAF50';
        console.log('Volume restored to:', Math.round(video.volume * 100) + '%');
    }, 5000);

    setTimeout(() => {
        overlay.remove();
        console.log('Demo complete');
    }, 7000);

} else {
    console.error('No video found!');
}