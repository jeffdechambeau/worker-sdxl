#!/bin/bash

echo "Worker Initiated"

echo "Starting WebUI API"
python stable-diffusion-webui/webui.py --api --no-half --disable-nan-check 

echo "Starting RunPod Handler"
python /rp_handler.py