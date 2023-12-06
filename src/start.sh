#!/bin/bash

echo "Worker Initiated"
echo "Starting WebUI API"

cd /stable-diffusion-webui
source venv/bin/activate

# We start the SD generation webui in the background and redirect the output to a log file

python3.10 /stable-diffusion-webui/launch.py --api --port 3000 > /workspace/webui-api.log 2>&1 &


echo "Starting RunPod Handler"
python3 -u /rp_handler.py