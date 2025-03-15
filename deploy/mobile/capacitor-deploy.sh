#!/bin/bash

# deploy/mobile/capacitor-deploy.sh
# Basic script to build and deploy the Vacation Planner mobile app with Capacitor.
# Run this from the frontend/mobile/ directory after building the web app.

# Ensure dependencies are installed
echo "Installing dependencies..."
npm install

# Build the web app (assumes web/ is sibling directory)
echo "Building web assets..."
cd ../web
npm run build

# Sync web assets to Capacitor
echo "Syncing with Capacitor..."
cd ../mobile
npx cap sync

# Build and open for iOS (comment out if not needed)
echo "Building for iOS..."
npx cap open ios
# Uncomment to build IPA: npx cap run ios --release

# Build and open for Android (comment out if not needed)
# echo "Building for Android..."
# npx cap open android
# Uncomment to build APK: npx cap run android --release

echo "Deployment steps complete. Customize this script for your platform and signing needs."

# Notes#!/bin/bash

# deploy/mobile/capacitor-deploy.sh
# Basic script to build and deploy the Vacation Planner mobile app with Capacitor.
# Run this from the frontend/mobile/ directory after building the web app.

# Ensure dependencies are installed
echo "Installing dependencies..."
npm install

# Build the web app (assumes web/ is sibling directory)
echo "Building web assets..."
cd ../web
npm run build

# Sync web assets to Capacitor
echo "Syncing with Capacitor..."
cd ../mobile
npx cap sync

# Build and open for iOS (comment out if not needed)
echo "Building for iOS..."
npx cap open ios
# Uncomment to build IPA: npx cap run ios --release

# Build and open for Android (comment out if not needed)
# echo "Building for Android..."
# npx cap open android
# Uncomment to build APK: npx cap run android --release

echo "Deployment steps complete. Customize this script for your platform and signing needs."

# Notes
