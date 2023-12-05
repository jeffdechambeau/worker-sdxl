#!/bin/bash

echo "Worker Initiated"

echo "Starting WebUI API"

source /venv/bin/activate
python3.10 /stable-diffusion-webui/webui.py --skip-python-version-check --skip-torch-cuda-test --port 3000 --api --nowebui --no-download-sd-model &

echo "Starting RunPod Handler"
python3 -u /rp_handler.py