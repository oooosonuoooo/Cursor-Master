#!/bin/bash

echo "[*] INSTALLING DEPENDENCIES..."
echo "    (You might be asked for your password)"
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3-tk imagemagick x11-apps
fi

echo "[*] CONFIGURING PERMISSIONS..."
# Create the icons directory if it doesn't exist
mkdir -p ~/.icons

# CRITICAL: Ensure the current user owns their own icons folder
# This fixes the "Permission Denied" errors
sudo chown -R $USER:$USER ~/.icons
chmod -R 755 ~/.icons

echo "[*] SETTING UP APP..."
chmod +x main.py

echo "---------------------------------------"
echo "[SUCCESS] Installation Complete!"
echo "Run the app with: ./main.py"
echo "---------------------------------------"