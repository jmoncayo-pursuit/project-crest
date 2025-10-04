#!/usr/bin/env python3
"""
Simple test server to verify basic functionality
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/data', methods=['POST'])
def data():
    data = request.get_json()
    text = data.get('text', '') if data else ''
    
    # Simple rule-based detection
    loud_keywords = ['[explosion]', '[gunshot]', '[thunder]', '[crash]', '[bang]', '[boom]']
    
    is_loud = any(keyword in text.lower() for keyword in loud_keywords)
    
    if is_loud:
        return jsonify({
            "action": "LOWER_VOLUME",
            "level": 0.3,
            "duration": 3000,
            "confidence": "YES",
            "text": text
        })
    else:
        return jsonify({
            "action": "NONE",
            "confidence": "NO",
            "text": text
        })

@app.route('/audio-data', methods=['POST'])
def audio_data():
    data = request.get_json()
    volume = data.get('volume', 0)
    spike = data.get('spike', 0)
    
    # Simple heuristic
    if spike > 0.3 or volume > 0.7:
        return jsonify({
            "action": "LOWER_VOLUME",
            "level": 0.25,
            "duration": 3000,
            "confidence": "YES"
        })
    else:
        return jsonify({
            "action": "NONE",
            "confidence": "NO"
        })

if __name__ == '__main__':
    print("🚀 Starting simple test server on port 5003...")
    app.run(debug=False, host='0.0.0.0', port=5003)