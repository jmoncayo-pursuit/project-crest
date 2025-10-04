// Live YouTube AI Tester
// Run this in the browser console while on a YouTube page to test AI decisions

console.log("🚀 Crest Live YouTube AI Tester Loaded!");

class CrestLiveTester {
    constructor() {
        this.decisions = [];
        this.isMonitoring = false;
        this.testResults = {
            total: 0,
            volumeChanges: 0,
            correctPredictions: 0
        };

        this.setupUI();
    }

    setupUI() {
        // Create test panel
        const panel = document.createElement('div');
        panel.id = 'crest-test-panel';
        panel.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            width: 350px;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10001;
            border: 2px solid #00ff88;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        `;

        panel.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 10px; color: #00ff88;">
                🧪 CREST AI LIVE TESTER
            </div>
            <div id="test-stats">
                <div>Decisions Tested: <span id="total-count">0</span></div>
                <div>Volume Changes: <span id="volume-count">0</span></div>
                <div>Accuracy: <span id="accuracy">N/A</span></div>
            </div>
            <div style="margin: 10px 0;">
                <button id="start-monitoring" style="background: #00ff88; color: black; border: none; padding: 5px 10px; border-radius: 5px; margin-right: 5px;">Start Monitoring</button>
                <button id="stop-monitoring" style="background: #ff4444; color: white; border: none; padding: 5px 10px; border-radius: 5px; margin-right: 5px;">Stop</button>
                <button id="clear-results" style="background: #666; color: white; border: none; padding: 5px 10px; border-radius: 5px;">Clear</button>
            </div>
            <div id="recent-decisions" style="max-height: 200px; overflow-y: auto; border-top: 1px solid #333; padding-top: 10px;">
                <div style="color: #888;">Recent AI decisions will appear here...</div>
            </div>
        `;

        document.body.appendChild(panel);

        // Add event listeners
        document.getElementById('start-monitoring').onclick = () => this.startMonitoring();
        document.getElementById('stop-monitoring').onclick = () => this.stopMonitoring();
        document.getElementById('clear-results').onclick = () => this.clearResults();

        console.log("✅ Test panel created - look for it in the top-right corner");
    }

    startMonitoring() {
        if (this.isMonitoring) return;

        this.isMonitoring = true;
        console.log("🔍 Starting AI decision monitoring...");

        // Monitor subtitle changes
        this.subtitleObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList.contains('ytp-caption-segment')) {
                        const subtitleText = node.textContent;
                        this.testSubtitle(subtitleText);
                    }
                });
            });
        });

        // Start observing
        const captionWindow = document.querySelector('.ytp-caption-window-container');
        if (captionWindow) {
            this.subtitleObserver.observe(captionWindow, { childList: true, subtree: true });
            console.log("✅ Subtitle monitoring active");
        } else {
            console.log("⚠️ No captions found - make sure subtitles are enabled");
        }

        // Update UI
        document.getElementById('start-monitoring').style.background = '#666';
        document.getElementById('start-monitoring').textContent = 'Monitoring...';
    }

    stopMonitoring() {
        if (!this.isMonitoring) return;

        this.isMonitoring = false;

        if (this.subtitleObserver) {
            this.subtitleObserver.disconnect();
        }

        console.log("⏹️ Monitoring stopped");

        // Update UI
        document.getElementById('start-monitoring').style.background = '#00ff88';
        document.getElementById('start-monitoring').textContent = 'Start Monitoring';
    }

    async testSubtitle(subtitleText) {
        if (!subtitleText || subtitleText.trim().length === 0) return;

        console.log(`🧪 Testing subtitle: "${subtitleText}"`);

        try {
            // Send to AI server
            const response = await fetch('http://localhost:5003/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: subtitleText })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const result = await response.json();

            // Analyze decision
            const decision = result.action === 'LOWER_VOLUME' ? 'LOWER_VOLUME' : 'NO_ACTION';
            const timestamp = new Date().toLocaleTimeString();

            // Determine if this should be a loud event (simple heuristic for testing)
            const isLoudEvent = this.isLikelyLoudEvent(subtitleText);
            const isCorrect = (isLoudEvent && decision === 'LOWER_VOLUME') ||
                (!isLoudEvent && decision === 'NO_ACTION');

            // Store result
            const testResult = {
                timestamp,
                subtitle: subtitleText,
                decision,
                isLoudEvent,
                isCorrect,
                level: result.level,
                duration: result.duration
            };

            this.decisions.push(testResult);
            this.updateStats();
            this.displayDecision(testResult);

        } catch (error) {
            console.error('❌ Error testing subtitle:', error);
            this.displayError(subtitleText, error.message);
        }
    }

    isLikelyLoudEvent(text) {
        // Simple heuristic to determine if subtitle describes a loud event
        const loudKeywords = [
            'explosion', 'gunshot', 'thunder', 'crash', 'bang', 'boom',
            'screaming', 'shouting', 'dramatic music', 'intense music',
            '[explosion]', '[gunshot]', '[thunder]', '[crash]', '[bang]',
            '[boom]', '[screaming]', '[shouting]', '[dramatic music]'
        ];

        const lowerText = text.toLowerCase();
        return loudKeywords.some(keyword => lowerText.includes(keyword));
    }

    updateStats() {
        this.testResults.total = this.decisions.length;
        this.testResults.volumeChanges = this.decisions.filter(d => d.decision === 'LOWER_VOLUME').length;
        this.testResults.correctPredictions = this.decisions.filter(d => d.isCorrect).length;

        const accuracy = this.testResults.total > 0 ?
            (this.testResults.correctPredictions / this.testResults.total * 100).toFixed(1) : 'N/A';

        // Update UI
        document.getElementById('total-count').textContent = this.testResults.total;
        document.getElementById('volume-count').textContent = this.testResults.volumeChanges;
        document.getElementById('accuracy').textContent = accuracy + '%';
    }

    displayDecision(result) {
        const container = document.getElementById('recent-decisions');

        // Clear placeholder text
        if (container.children.length === 1 && container.children[0].style.color === 'rgb(136, 136, 136)') {
            container.innerHTML = '';
        }

        const decisionDiv = document.createElement('div');
        decisionDiv.style.cssText = `
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 5px;
            border-left: 3px solid ${result.isCorrect ? '#00ff88' : '#ff4444'};
            background: rgba(255,255,255,0.05);
        `;

        const icon = result.decision === 'LOWER_VOLUME' ? '🔉' : '🔊';
        const correctIcon = result.isCorrect ? '✅' : '❌';

        decisionDiv.innerHTML = `
            <div style="font-weight: bold;">
                ${icon} ${result.timestamp} ${correctIcon}
            </div>
            <div style="color: #ccc; font-size: 11px;">
                "${result.subtitle.substring(0, 40)}${result.subtitle.length > 40 ? '...' : ''}"
            </div>
            <div style="color: ${result.decision === 'LOWER_VOLUME' ? '#ffaa00' : '#88ff88'}; font-size: 11px;">
                Decision: ${result.decision}
                ${result.level ? ` (${result.level})` : ''}
            </div>
        `;

        container.insertBefore(decisionDiv, container.firstChild);

        // Keep only last 10 decisions visible
        while (container.children.length > 10) {
            container.removeChild(container.lastChild);
        }
    }

    displayError(subtitle, error) {
        const container = document.getElementById('recent-decisions');

        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 5px;
            border-left: 3px solid #ff4444;
            background: rgba(255,0,0,0.1);
        `;

        errorDiv.innerHTML = `
            <div style="font-weight: bold; color: #ff4444;">
                ❌ ${new Date().toLocaleTimeString()} ERROR
            </div>
            <div style="color: #ccc; font-size: 11px;">
                "${subtitle.substring(0, 40)}${subtitle.length > 40 ? '...' : ''}"
            </div>
            <div style="color: #ff8888; font-size: 11px;">
                ${error}
            </div>
        `;

        container.insertBefore(errorDiv, container.firstChild);
    }

    clearResults() {
        this.decisions = [];
        this.testResults = { total: 0, volumeChanges: 0, correctPredictions: 0 };
        this.updateStats();

        const container = document.getElementById('recent-decisions');
        container.innerHTML = '<div style="color: #888;">Recent AI decisions will appear here...</div>';

        console.log("🗑️ Test results cleared");
    }
}

// Initialize the tester
window.crestTester = new CrestLiveTester();

console.log("✅ Crest Live Tester ready!");
console.log("📋 Instructions:");
console.log("1. Make sure your Flask server is running (localhost:5003)");
console.log("2. Enable YouTube subtitles on this video");
console.log("3. Click 'Start Monitoring' in the test panel");
console.log("4. Watch the AI decisions in real-time!");
console.log("5. Look for accuracy percentage - high accuracy means it's working intelligently");