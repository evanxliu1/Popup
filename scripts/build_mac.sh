#!/bin/bash
# Build DesktopNoti as a Mac .app using PyInstaller
# Usage: ./build_mac.sh

set -e

# Clean previous build
echo "Cleaning previous build..."
rm -rf dist build DesktopNoti.spec

# Build with PyInstaller
echo "Building with PyInstaller..."
pyinstaller \
  --windowed \
  --name DesktopNoti \
  --icon assets/app_icon.icns \
  --add-data "config/config.json:config" \
  --add-data "config/credentials.json:config" \
  --add-data "config/token.json:config" \
  --add-data "assets/icon_1024.png:assets" \
  notification/main.py

# Move .app to top-level for drag-and-drop
if [ -d "dist/DesktopNoti.app" ]; then
  mv dist/DesktopNoti.app .
  echo "DesktopNoti.app created!"
else
  echo "Build failed: .app not found."
  exit 1
fi
