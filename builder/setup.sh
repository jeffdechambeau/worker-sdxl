#!/bin/bash

# Stop script on error
set -e

# Update System
apt-get update && apt-get upgrade -y

# Install System Dependencies
apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    git \
    wget \
    openssh-server \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update && apt-get install -y --no-install-recommends python3.10 python3.10-dev python3.10-distutils

# Install pip for Python 3.10
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.10 get-pip.py

# Clean up
apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /get-pip.py
