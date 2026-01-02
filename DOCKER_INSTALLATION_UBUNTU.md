# Docker Installation Guide for Ubuntu Linux

Complete step-by-step guide to install Docker and Docker Compose on Ubuntu.

---

## Prerequisites

- Ubuntu 20.04 LTS or newer
- sudo privileges
- Internet connection

---

## Step 1: Remove Old Docker Versions (Optional)

If you have old Docker versions installed:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

---

## Step 2: Set Up Docker Repository

### 1. Update package index

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

### 2. Add Docker GPG key

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### 3. Set up stable repository

```bash
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## Step 3: Install Docker Engine

### 1. Update package index again

```bash
sudo apt-get update
```

### 2. Install Docker

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Verify installation

```bash
docker --version
docker run hello-world
```

You should see:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Step 4: Install Docker Compose (Standalone)

### Option A: Latest version from GitHub (Recommended)

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Option B: Using apt (if not already installed)

```bash
sudo apt-get install -y docker-compose
docker-compose --version
```

---

## Step 5: Manage Docker as Non-Root User

By default, Docker requires `sudo`. To run without sudo:

### 1. Create docker group (if it doesn't exist)

```bash
sudo groupadd 
```

### 2. Add your user to the docker group

```bash
sudo usermod -aG docker $USER
```

### 3. Apply new group membership

```bash
newgrp docker
```

### 4. Verify (no sudo needed)

```bash
docker run hello-world
```
docker
### 5. Log out and back in (if it still asks for sudo)

```bash
logout
# Then log back in
```

---

## Step 6: Enable Docker to Start on Boot

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

---

## Verify Installation

Run these commands to verify everything is working:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Check Docker info
docker info

# Run a test container
docker run --rm hello-world
```

Expected output:
```
Docker version 24.0.x, build xxxxx
Docker Compose version v2.x.x
...
Hello from Docker!
```

---

## Quick Commands Reference

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View Docker images
docker images

# Pull an image
docker pull ubuntu

# Build an image
docker build -t myapp:latest .

# Run a container
docker run -d -p 8000:8000 myapp:latest

# View logs
docker logs <container_id>

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Docker Compose up
docker-compose up -d

# Docker Compose down
docker-compose down
```

---

## Uninstall Docker (If needed)

```bash
# Uninstall Docker packages
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Remove Docker data
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## Troubleshooting

### Problem: Permission denied while trying to connect to Docker daemon

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: Docker service won't start

**Solution:**
```bash
# Restart Docker service
sudo systemctl restart docker

# Check status
sudo systemctl status docker

# View service logs
sudo journalctl -u docker -n 50
```

### Problem: Cannot connect to Docker daemon

**Solution:**
```bash
# Make sure Docker is running
sudo systemctl start docker

# Check if socket exists
ls -la /var/run/docker.sock
```

---

## Next Steps

After installation, you can now use Docker with your Library API:

```bash
# Navigate to your project
cd ~/library-api-project

# Build and run with Docker Compose
docker-compose up -d

# Access the API
curl http://localhost:8000

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## Additional Resources

- **Official Docker Documentation:** https://docs.docker.com/
- **Docker Compose Documentation:** https://docs.docker.com/compose/
- **Docker Hub:** https://hub.docker.com/
- **Ubuntu Docker Installation:** https://docs.docker.com/engine/install/ubuntu/

---

## Installation Complete!

Your Docker setup is ready. You can now containerize and run your Library API backend!
