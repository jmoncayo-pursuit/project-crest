#!/usr/bin/env python3
"""
Simple demo startup script that loads environment and starts server
"""
import os
import subprocess
import sys

def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    print(f"✅ Loaded {key}")
        return True
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
        return False

def main():
    print("🚀 Starting Crest Demo Server")
    print("=" * 40)
    
    # Load environment
    if load_env_file():
        print("✅ Environment variables loaded")
    else:
        print("⚠️  Running without .env file")
    
    print("\n🔥 Starting Flask server on port 5003...")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == '__main__':
    main()