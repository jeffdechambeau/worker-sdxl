#!/bin/bash

# Stop script on error
set -e

# Install System Dependencies
apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    git \
    wget \
    openssh-server \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update && apt-get install -y python3.10 python3.10-dev python3.10-distutils

# Update Python 3 alternatives to point to Python 3.10
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install pip for Python 3.10
apt-get install -y python3-pip

# Clean up
apt-get clean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
