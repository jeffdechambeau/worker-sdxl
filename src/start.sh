#!/bin/bash

echo "Starting Worker"
echo "Optionally grabbing models"
./setup.sh

mkdir -p /workspace/logs

echo "Starting WebUI API"
source /venv/stable-diffusion-webui/bin/activate
python3.10 /workspace/stable-diffusion-webui/webui.py --api --nowebui --port 3000 > /workspace/logs/webui-api.log 2>&1 &
deactivate

echo "Starting RunPod Handler"
python3 -u /rp_handler.py