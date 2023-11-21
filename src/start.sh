#!/bin/bash

echo "Worker Initiated"

echo "Starting WebUI API"
python3 /workspace/stable-diffusion-webui/webui.py --api --no-half --disable-nan-check 

echo "Starting RunPod Handler"
python3 -u /rp_handler.py