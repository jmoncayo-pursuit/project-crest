#!/usr/bin/env python3
"""
Minimal version of app.py for testing - no Datadog blocking
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "port": 5003})

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text', '') if data else ''
        
        # Simple mock logic
        if any(keyword in text.lower() for keyword in ['explosion', 'gunshot', 'dramatic music']):
            return jsonify({
                "action": "LOWER_VOLUME",
                "level": 0.3,
                "duration": 5000,
                "confidence": "YES"
            })
        else:
            return jsonify({
                "action": "NONE",
                "confidence": "NO"
            })
    else:
        return jsonify({"message": "Hello"})

@app.route('/feedback', methods=['POST'])
def feedback():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("🚀 Starting minimal server on port 5003...")
    app.run(debug=True, host='0.0.0.0', port=5003)