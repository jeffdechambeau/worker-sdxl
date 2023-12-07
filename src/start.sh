#!/bin/bash
echo "Starting Worker"
echo "Optionally grabbing models"
./setup.sh

echo "Worker Initiated"
echo "Starting WebUI API"

cd /stable-diffusion-webui
source venv/bin/activate

# We start the SD generation webui in the background and redirect the output to a log file
mkdir -p /workspace/logs
python3.10 /stable-diffusion-webui/webui.py --api --nowebui --port 3000 > /workspace/logs/webui-api.log 2>&1 &
deactivate

echo "Starting RunPod Handler"
python3 -u /rp_handler.py