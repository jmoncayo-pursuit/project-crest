#!/usr/bin/env python3
"""
Project Crest Startup Script
Starts the Flask server with proper Datadog tracing and environment setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check environment variables and determine mode"""
    truefoundry_vars = [
        'TRUEFOUNDRY_API_KEY',
        'TRUEFOUNDRY_BASE_URL'
    ]
    
    missing_vars = []
    for var in truefoundry_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing TrueFoundry environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n🔧 Server will start in MOCK MODE")
        print("   - Uses rule-based logic instead of AI")
        print("   - Perfect for testing and demos")
        print("\n💡 To enable LIVE MODE, set:")
        print("   export TRUEFOUNDRY_API_KEY='tfy-your-key'")
        print("   export TRUEFOUNDRY_BASE_URL='https://your-endpoint'")
        return "mock"
    
    print("✅ TrueFoundry credentials found - LIVE MODE enabled")
    return "live"

def check_dependencies():
    """Check if required Python packages are installed"""
    try:
        import flask
        import flask_cors
        import openai
        import datadog
        import ddtrace
        print("✅ All Python dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def start_server():
    """Start the Flask server with Datadog tracing"""
    print("🚀 Starting Project Crest server with Datadog tracing...")
    print("📊 Server will be available at: http://localhost:5003")
    print("📈 Datadog metrics will be sent to localhost:8125")
    print("🔍 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start with ddtrace-run for Datadog APM
        subprocess.run([
            "ddtrace-run", 
            "python", 
            "app.py"
        ], check=True)
    except subprocess.CalledProcessError:
        print("\n❌ Failed to start with ddtrace-run")
        print("Falling back to regular Python execution...")
        try:
            subprocess.run(["python", "app.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to start server")
            return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except FileNotFoundError:
        print("❌ ddtrace-run not found. Install with: pip install ddtrace")
        print("Trying regular Python execution...")
        try:
            subprocess.run(["python", "app.py"], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            return True
    
    return True

def main():
    """Main startup function"""
    print("🎯 Project Crest - AI Volume Control")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check environment variables and determine mode
    mode = check_environment()
    if mode == "mock":
        print("🎭 Starting in MOCK MODE - No API calls will be made")
    elif mode == "live":
        print("🚀 Starting in LIVE MODE - AI Gateway enabled")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Set default Datadog environment variables if not set
    os.environ.setdefault('DD_AGENT_HOST', 'localhost')
    os.environ.setdefault('DD_LOGS_INJECTION', 'true')
    os.environ.setdefault('DD_SERVICE', 'crest-agent')
    os.environ.setdefault('DD_ENV', 'development')
    os.environ.setdefault('DD_VERSION', '0.1.0')
    
    print("✅ Environment check passed")
    print("✅ Dependencies check passed")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()