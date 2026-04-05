# OAKCRED.GLOBAL - EC2 INITIAL SETUP SCRIPT
# Run this once on a fresh Ubuntu 22.04 or Amazon Linux 2023 instance.

echo "--- Initializing OAKCRED Server Environment ---"

# 1. Create 2GB Swap File (Crucial for Micro Instances to prevent OOM)
if [ ! -f /swapfile ]; then
    echo "Creating 2GB Swap File for Memory Boost..."
    sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 2. Update System
sudo dnf update -y || sudo apt-get update -y

# 3. Install Python & Build Tools
sudo dnf install -y python3-pip python3-devel git gcc-c++ || sudo apt-get install -y python3-pip python3-venv git build-essential

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
