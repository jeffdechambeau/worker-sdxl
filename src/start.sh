#!/bin/bash

echo "Starting Worker"
echo "Optionally grabbing models"
./setup.sh

cd /stable-diffusion-webui
source venv/bin/activate

echo "Starting WebUI API"
mkdir -p /workspace/logs
python3.10 /stable-diffusion-webui/webui.py --api --nowebui --port 3000 > /workspace/logs/webui-api.log 2>&1 &
deactivate

echo "Starting RunPod Handler"
source /kohya_ss/env/bin/activate
python3 -u /rp_handler.py