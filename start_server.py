#!/usr/bin/env python3
"""
Startup script for Crest Flask server with Datadog tracing
Use this instead of running app.py directly for full observability
"""
import os
import subprocess
import sys

def set_environment_variables():
    """Set default environment variables for Datadog"""
    env_vars = {
        'DD_SERVICE': 'crest-agent',
        'DD_ENV': 'development', 
        'DD_VERSION': '0.1.0',
        'DD_LOGS_INJECTION': 'true',
        'DD_AGENT_HOST': 'localhost'
    }
    
    for key, default_value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = default_value
            print(f"Set {key}={default_value}")

def main():
    print("🚀 Starting Crest Flask Server with Datadog Observability")
    print("=" * 60)
    
    # Set environment variables
    set_environment_variables()
    
    # Check if ddtrace is available
    try:
        import ddtrace
        print("✅ ddtrace available - starting with APM instrumentation")
        
        # Start with ddtrace-run for automatic instrumentation
        cmd = [sys.executable, '-m', 'ddtrace.commands.ddtrace_run', sys.executable, 'app.py']
        print(f"Command: {' '.join(cmd)}")
        print("=" * 60)
        
        # Execute with ddtrace-run
        subprocess.run(cmd)
        
    except ImportError:
        print("⚠️  ddtrace not available - starting without APM instrumentation")
        print("Install with: pip install ddtrace")
        print("=" * 60)
        
        # Fallback to regular Python
        subprocess.run([sys.executable, 'app.py'])

if __name__ == '__main__':
    main()