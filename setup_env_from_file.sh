#!/bin/bash
# Load environment variables from .env file

if [ -f ".env" ]; then
    echo "🔧 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
    
    # Verify required variables are set
    echo ""
    echo "🔍 Verifying required variables:"
    
    if [ -n "$TRUEFOUNDRY_API_KEY" ]; then
        echo "✅ TRUEFOUNDRY_API_KEY is set"
    else
        echo "❌ TRUEFOUNDRY_API_KEY is missing"
    fi
    
    if [ -n "$TRUEFOUNDRY_BASE_URL" ]; then
        echo "✅ TRUEFOUNDRY_BASE_URL is set"
    else
        echo "❌ TRUEFOUNDRY_BASE_URL is missing"
    fi
    
    echo "✅ DD_SERVICE=$DD_SERVICE"
    echo "✅ DD_ENV=$DD_ENV"
    echo "✅ DD_VERSION=$DD_VERSION"
    echo "✅ DD_LOGS_INJECTION=$DD_LOGS_INJECTION"
    echo "✅ DD_AGENT_HOST=$DD_AGENT_HOST"
    
    echo ""
    echo "🚀 Ready to start server with: python start_crest.py"
else
    echo "❌ .env file not found"
    echo "📋 Create .env file from .env.example:"
    echo "   cp .env.example .env"
    echo "   # Edit .env with your actual credentials"
fi