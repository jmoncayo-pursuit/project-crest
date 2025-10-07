// popup.js - Activity log and stats for Crest extension

let adjustmentCount = 0;
let lastActionTime = '--';

// Load saved data
chrome.storage.local.get(['adjustmentCount', 'activityLog'], (result) => {
    adjustmentCount = result.adjustmentCount || 0;
    document.getElementById('adjustments-count').textContent = adjustmentCount;

    if (result.activityLog) {
        const logContainer = document.getElementById('activity-log');
        logContainer.innerHTML = result.activityLog;
    }
});

// Listen for log events from service worker
chrome.runtime.onMessage.addListener((message) => {
    // Handle legacy LOG_EVENT messages
    if (message.type === 'LOG_EVENT') {
        addLogEntry(message.text);

        // Update stats if it's a volume adjustment
        if (message.text.includes('lowered volume')) {
            adjustmentCount++;
            lastActionTime = new Date().toLocaleTimeString();

            document.getElementById('adjustments-count').textContent = adjustmentCount;
            document.getElementById('last-action').textContent = lastActionTime;

            // Update status
            const status = document.getElementById('status');
            status.className = 'status active';
            status.textContent = '🎵 Agent actively managing volume';

            // Reset status after 5 seconds
            setTimeout(() => {
                status.className = 'status inactive';
                status.textContent = '🔍 Monitoring for loud audio events...';
            }, 5000);

            // Save stats
            chrome.storage.local.set({ adjustmentCount });
        }
    }
    // Handle enhanced DASHBOARD_UPDATE messages
    else if (message.type === 'DASHBOARD_UPDATE') {
        if (message.event && message.event.type === 'volume_adjustment') {
            adjustmentCount++;
            lastActionTime = new Date().toLocaleTimeString();

            document.getElementById('adjustments-count').textContent = adjustmentCount;
            document.getElementById('last-action').textContent = lastActionTime;

            // Add log entry
            addLogEntry(message.event.message || `🎵 Volume adjusted (${message.event.trigger})`);

            // Update status
            const status = document.getElementById('status');
            status.className = 'status active';
            status.textContent = '🎵 Agent actively managing volume';

            // Reset status after 5 seconds
            setTimeout(() => {
                status.className = 'status inactive';
                status.textContent = '🔍 Monitoring for loud audio events...';
            }, 5000);

            // Save stats
            chrome.storage.local.set({ adjustmentCount });
        } else if (message.event) {
            // Log other events
            addLogEntry(message.event.message || `${message.event.type}: ${message.event.trigger || 'system'}`);
        }
    }
});

function addLogEntry(text) {
    const logContainer = document.getElementById('activity-log');
    const entry = document.createElement('div');
    entry.className = 'log-entry';

    const time = new Date().toLocaleTimeString();
    entry.innerHTML = `
        <div class="log-time">${time}</div>
        <div>${text}</div>
    `;

    // Add to top
    logContainer.insertBefore(entry, logContainer.firstChild);

    // Keep only last 20 entries
    while (logContainer.children.length > 20) {
        logContainer.removeChild(logContainer.lastChild);
    }

    // Save log
    chrome.storage.local.set({ activityLog: logContainer.innerHTML });
}

// Clear log button
document.getElementById('clear-log').addEventListener('click', () => {
    document.getElementById('activity-log').innerHTML = `
        <div class="log-entry">
            <div class="log-time">Log cleared</div>
            <div>Activity log has been cleared</div>
        </div>
    `;

    adjustmentCount = 0;
    lastActionTime = '--';

    document.getElementById('adjustments-count').textContent = '0';
    document.getElementById('last-action').textContent = '--';

    chrome.storage.local.clear();
});

// Test button for demo purposes
document.addEventListener('dblclick', () => {
    addLogEntry('🧪 Test entry - Double-clicked popup for demo');
});