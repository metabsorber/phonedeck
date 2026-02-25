#!/usr/bin/env bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Build React frontend (CI=false to treat warnings as warnings, not errors)
cd frontend
CI=false npm run build
cd ..

# Move build to where Flask expects it
cp -r frontend/build ./build
