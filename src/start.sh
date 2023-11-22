#!/bin/bash
echo "Worker Initiated"

pip install -U pip
pip install -U httpcore
pip install -U open-clip-torch
pip install -U rich

echo "Starting WebUI API"
python3 /workspace/sd/stable-diffusion-webui/webui.py --api --no-half --disable-nan-check 

echo "Starting RunPod Handler"
python3 -u /rp_handler.py