#!/bin/bash
echo "In src/start.sh"
echo "Contents of /"
ls /

echo "Contents of /workspace"
ls /workspace

echo "Worker Initiated"

echo "Starting WebUI API"
python3 /workspace/stable-diffusion-webui/webui.py --api --no-half --disable-nan-check 

echo "Starting RunPod Handler"
python3 -u /rp_handler.py