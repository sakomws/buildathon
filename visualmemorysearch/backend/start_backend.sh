#!/bin/bash

# Set environment variables for the backend
export SECRET_KEY="your-secret-key-change-in-production-12345"
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:3000/auth/google/callback"
export GOOGLE_REDIRECT_URI_BACKEND="http://localhost:8000/auth/google/callback"

# Start the backend server
echo "Starting Visual Memory Search Backend..."
echo "Environment variables set:"
echo "  SECRET_KEY: Set"
echo "  GOOGLE_CLIENT_ID: Set"
echo "  GOOGLE_CLIENT_SECRET: Set"
echo "  GOOGLE_REDIRECT_URI: $GOOGLE_REDIRECT_URI"
echo "  GOOGLE_REDIRECT_URI_BACKEND: $GOOGLE_REDIRECT_URI_BACKEND"
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
