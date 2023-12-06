#!/bin/bash

echo "Worker Initiated"
echo "Starting WebUI API"

source /venv/bin/activate

# We start the SD generation webui in the background and redirect the output to a log file
python3.10 /stable-diffusion-webui/webui.py \ 
    --skip-python-version-check \
    --skip-torch-cuda-test \
    --nowebui \
    --api \
    --port 3000 \ 
    --no-download-sd-model \
    > /workspace/webui-api.log 2>&1 &


echo "Starting RunPod Handler"
python3 -u /rp_handler.py