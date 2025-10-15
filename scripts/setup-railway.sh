#!/bin/bash

# Setup Railway project for the first time
set -e

echo "🛤️  Setting up Railway project..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -fsSL https://railway.app/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Login to Railway
echo "🔐 Logging in to Railway..."
railway login

# Initialize Railway project
if [ ! -f "railway.toml" ]; then
    echo "❌ railway.toml not found. Make sure you're in the right directory."
    exit 1
fi

echo "📦 Initializing Railway project..."
railway init

# Add PostgreSQL service
echo "🗄️  Adding PostgreSQL service..."
railway add postgresql

# Set environment variables
echo "⚙️  Setting environment variables..."
railway variables set ENVIRONMENT=production
railway variables set PORT=8000
railway variables set ENABLE_ANALYTICS=true
railway variables set ENABLE_FEEDBACK=true
railway variables set INCREMENT_VIEWS_ONLY_IN_PRODUCTION=true

# Generate a secure secret key
echo "🔑 Generating secret key..."
SECRET_KEY=$(openssl rand -hex 32)
railway variables set SECRET_KEY=$SECRET_KEY

echo "✅ Railway project setup complete!"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. The CI/CD pipeline will automatically deploy to Railway"
echo "3. Check Railway dashboard for your deployment URL"
echo ""
echo "To deploy manually, run: ./scripts/deploy.sh"