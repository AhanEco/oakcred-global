#!/bin/bash

# OAKCRED.GLOBAL - EC2 INITIAL SETUP SCRIPT
# Run this once on a fresh Ubuntu 22.04 instance.

echo "--- Initializing OAKCRED Server Environment ---"

# 1. Update System
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Python & Build Tools
sudo apt-get install -y python3-pip python3-venv git build-essential

# 3. Install Node.js & PM2 (for process management)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2

# 4. Create App Directory
mkdir -p ~/oakcred
cd ~/oakcred

echo "--- Backend Environment Ready ---"
echo "Instructions:"
echo "1. Clone your repo: git clone https://github.com/[your-user]/oakcred-global.git ."
echo "2. Create venv: python3 -m venv venv"
echo "3. Update task.md for CI/CD secrets setup."
