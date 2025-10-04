#!/bin/bash
# Environment setup script for Crest backend

echo "🚀 Setting up Crest Backend Environment"
echo "======================================"

# Datadog environment variables
export DD_SERVICE="crest-agent"
export DD_ENV="development"
export DD_VERSION="0.1.0"
export DD_LOGS_INJECTION="true"
export DD_AGENT_HOST="localhost"

echo "✅ Datadog environment variables set:"
echo "   DD_SERVICE=$DD_SERVICE"
echo "   DD_ENV=$DD_ENV"
echo "   DD_VERSION=$DD_VERSION"
echo "   DD_LOGS_INJECTION=$DD_LOGS_INJECTION"
echo "   DD_AGENT_HOST=$DD_AGENT_HOST"

# Check if TrueFoundry variables are set
if [ -z "$TRUEFOUNDRY_API_KEY" ]; then
    echo "⚠️  TRUEFOUNDRY_API_KEY not set"
    echo "   Set it with: export TRUEFOUNDRY_API_KEY='your-api-key'"
else
    echo "✅ TRUEFOUNDRY_API_KEY is set"
fi

if [ -z "$TRUEFOUNDRY_BASE_URL" ]; then
    echo "⚠️  TRUEFOUNDRY_BASE_URL not set"
    echo "   Set it with: export TRUEFOUNDRY_BASE_URL='your-base-url'"
else
    echo "✅ TRUEFOUNDRY_BASE_URL is set"
fi

echo ""
echo "📋 To start the server with full observability:"
echo "   python start_server.py"
echo ""
echo "📋 To test the backend:"
echo "   python manual_test.py"