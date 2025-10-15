#!/bin/bash

# Deployment script for Railway
set -e

echo "🚀 Starting deployment process..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -fsSL https://railway.app/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Check if logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please run 'railway login' first."
    exit 1
fi

echo "✅ Railway CLI ready"

# Run tests first
echo "🧪 Running tests..."
python -m pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Aborting deployment."
    exit 1
fi

echo "✅ Tests passed"

# Deploy to Railway
echo "📦 Deploying to Railway..."
railway up

echo "⏳ Waiting for deployment to complete..."
sleep 30

# Get deployment URL
DEPLOYMENT_URL=$(railway domain --no-trunc 2>/dev/null | head -n1 || echo "")
if [ -n "$DEPLOYMENT_URL" ]; then
    echo "🌐 Deployment URL: $DEPLOYMENT_URL"

    # Health check
    echo "🏥 Running health check..."
    if curl -f "$DEPLOYMENT_URL/api/v1/health" > /dev/null 2>&1; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
        exit 1
    fi
else
    echo "⚠️ Could not get deployment URL"
fi

echo "🎉 Deployment completed successfully!"