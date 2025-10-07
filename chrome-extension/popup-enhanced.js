// popup-enhanced.js - Enhanced dashboard with real-time activity and metrics

class EnhancedDashboard {
    constructor() {
        this.events = [];
        this.stats = {
            totalAdjustments: 0,
            subtitleDetections: 0,
            audioDetections: 0,
            userCorrections: 0,
            lastActionTime: null,
            accuracyRate: 1.0,
            sessionDuration: 0
        };
        this.isConnected = false;
        this.updateInterval = null;
    }

    async initialize() {
        console.log('🚀 Initializing enhanced dashboard...');

        // Set up UI event listeners
        this.setupEventListeners();

        // Load initial data
        await this.loadDashboardData();

        // Start real-time updates
        this.startRealTimeUpdates();

        // Update display
        this.updateDisplay();

        console.log('✅ Enhanced dashboard initialized');
    }

    setupEventListeners() {
        // Clear log button
        const clearButton = document.getElementById('clear-log');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearLog());
        }

        // Test buttons for demo
        const testVolumeButton = document.getElementById('test-volume');
        if (testVolumeButton) {
            testVolumeButton.addEventListener('click', () => this.testVolumeControl());
        }

        const testAudioButton = document.getElementById('test-audio');
        if (testAudioButton) {
            testAudioButton.addEventListener('click', () => this.testAudioMonitoring());
        }

        // Refresh button
        const refreshButton = document.getElementById('refresh-data');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => this.loadDashboardData());
        }
    }

    async loadDashboardData() {
        try {
            const response = await chrome.runtime.sendMessage({
                type: 'GET_DASHBOARD_DATA'
            });

            if (response) {
                this.events = response.events || [];
                this.stats = response.stats || this.stats;
                this.isConnected = true;
                this.updateDisplay();
            }
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.isConnected = false;
            this.updateConnectionStatus();
        }
    }

    startRealTimeUpdates() {
        // Listen for real-time updates from service worker
        chrome.runtime.onMessage.addListener((message) => {
            if (message.type === 'DASHBOARD_UPDATE') {
                this.handleDashboardUpdate(message);
            }
        });

        // Periodic refresh
        this.updateInterval = setInterval(() => {
            this.updateSessionDuration();
            this.updateDisplay();
        }, 1000);
    }

    handleDashboardUpdate(message) {
        console.log('📊 Dashboard update received:', message);

        // Add new event
        if (message.event) {
            this.events.unshift(message.event);

            // Keep only last 20 events in popup
            if (this.events.length > 20) {
                this.events = this.events.slice(0, 20);
            }

            this.addEventToLog(message.event);
        }

        // Update stats
        if (message.stats) {
            this.stats = message.stats;
            this.updateStatsDisplay();
        }

        // Update status
        this.updateStatus(message.event);
    }

    updateDisplay() {
        this.updateStatsDisplay();
        this.updateConnectionStatus();
        this.updateEventLog();
    }

    updateStatsDisplay() {
        // Update main stats
        this.updateElement('adjustments-count', this.stats.totalAdjustments);
        this.updateElement('subtitle-count', this.stats.subtitleDetections);
        this.updateElement('audio-count', this.stats.audioDetections);
        this.updateElement('correction-count', this.stats.userCorrections);

        // Update accuracy rate
        const accuracyPercent = Math.round(this.stats.accuracyRate * 100);
        this.updateElement('accuracy-rate', `${accuracyPercent}%`);

        // Update last action time
        if (this.stats.lastActionTime) {
            const lastAction = new Date(this.stats.lastActionTime).toLocaleTimeString();
            this.updateElement('last-action', lastAction);
        } else {
            this.updateElement('last-action', '--');
        }

        // Update session duration
        this.updateSessionDuration();
    }

    updateSessionDuration() {
        if (this.stats.sessionStartTime) {
            const duration = Date.now() - this.stats.sessionStartTime;
            const minutes = Math.floor(duration / 60000);
            const seconds = Math.floor((duration % 60000) / 1000);
            this.updateElement('session-duration', `${minutes}:${seconds.toString().padStart(2, '0')}`);
        }
    }

    updateConnectionStatus() {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            if (this.isConnected) {
                statusElement.textContent = '🟢 Connected';
                statusElement.className = 'status connected';
            } else {
                statusElement.textContent = '🔴 Disconnected';
                statusElement.className = 'status disconnected';
            }
        }
    }

    updateStatus(event) {
        const statusElement = document.getElementById('status');
        if (!statusElement) return;

        if (event && event.type === 'volume_adjustment') {
            statusElement.className = 'status active';
            statusElement.textContent = `🎵 Active - ${event.trigger} detection`;

            // Reset status after 5 seconds
            setTimeout(() => {
                statusElement.className = 'status monitoring';
                statusElement.textContent = '🔍 Monitoring for loud events...';
            }, 5000);
        } else if (event && event.type === 'error') {
            statusElement.className = 'status error';
            statusElement.textContent = '⚠️ Error occurred';

            setTimeout(() => {
                statusElement.className = 'status monitoring';
                statusElement.textContent = '🔍 Monitoring for loud events...';
            }, 3000);
        }
    }

    updateEventLog() {
        const logContainer = document.getElementById('activity-log');
        if (!logContainer) return;

        logContainer.innerHTML = '';

        this.events.forEach(event => {
            this.addEventToLog(event);
        });
    }

    addEventToLog(event) {
        const logContainer = document.getElementById('activity-log');
        if (!logContainer) return;

        const entry = document.createElement('div');
        entry.className = `log-entry ${event.type}`;

        const time = new Date(event.timestamp).toLocaleTimeString();
        const confidence = event.confidence ? ` (${Math.round(event.confidence * 100)}%)` : '';

        entry.innerHTML = `
            <div class="log-header">
                <span class="log-time">${time}</span>
                <span class="log-type">${event.trigger || event.type}</span>
                ${confidence ? `<span class="log-confidence">${confidence}</span>` : ''}
            </div>
            <div class="log-message">${event.message}</div>
            ${event.aiReasoning ? `<div class="log-reasoning">💭 ${event.aiReasoning}</div>` : ''}
        `;

        // Add to top of log
        logContainer.insertBefore(entry, logContainer.firstChild);

        // Keep only last 20 entries visible
        while (logContainer.children.length > 20) {
            logContainer.removeChild(logContainer.lastChild);
        }
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    clearLog() {
        const logContainer = document.getElementById('activity-log');
        if (logContainer) {
            logContainer.innerHTML = `
                <div class="log-entry system">
                    <div class="log-header">
                        <span class="log-time">${new Date().toLocaleTimeString()}</span>
                        <span class="log-type">system</span>
                    </div>
                    <div class="log-message">📝 Activity log cleared</div>
                </div>
            `;
        }

        // Reset stats
        this.stats = {
            totalAdjustments: 0,
            subtitleDetections: 0,
            audioDetections: 0,
            userCorrections: 0,
            lastActionTime: null,
            accuracyRate: 1.0,
            sessionStartTime: Date.now()
        };

        this.updateStatsDisplay();

        // Clear storage
        chrome.storage.local.clear();
    }

    async testVolumeControl() {
        console.log('🧪 Testing volume control...');

        // Get active tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (tab && tab.url.includes('youtube.com')) {
            chrome.tabs.sendMessage(tab.id, {
                action: 'LOWER_VOLUME',
                level: 0.2,
                duration: 2000,
                confidence: 0.9,
                trigger: 'manual_test'
            });

            this.addEventToLog({
                type: 'test',
                trigger: 'manual',
                message: '🧪 Manual volume test executed',
                timestamp: Date.now(),
                confidence: 0.9
            });
        } else {
            this.addEventToLog({
                type: 'error',
                trigger: 'manual',
                message: '❌ Please navigate to a YouTube video first',
                timestamp: Date.now()
            });
        }
    }

    async testAudioMonitoring() {
        console.log('🧪 Testing audio monitoring...');

        // Get active tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (tab && tab.url.includes('youtube.com')) {
            // Send test message to content script
            chrome.tabs.sendMessage(tab.id, {
                action: 'TEST_AUDIO_MONITORING'
            });

            this.addEventToLog({
                type: 'test',
                trigger: 'manual',
                message: '🧪 Audio monitoring test requested',
                timestamp: Date.now()
            });
        } else {
            this.addEventToLog({
                type: 'error',
                trigger: 'manual',
                message: '❌ Please navigate to a YouTube video first',
                timestamp: Date.now()
            });
        }
    }

    cleanup() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Initialize dashboard when popup loads
let dashboard = null;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Enhanced popup loading...');

    dashboard = new EnhancedDashboard();
    await dashboard.initialize();
});

// Cleanup when popup closes
window.addEventListener('beforeunload', () => {
    if (dashboard) {
        dashboard.cleanup();
    }
});