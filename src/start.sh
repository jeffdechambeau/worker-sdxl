#!/bin/bash

echo "Starting Worker"
./setup.sh

mkdir -p /workspace/logs

# Convert IS_TRAINING_POD_ONLY to lowercase for case-insensitive comparison
isTrainingPodOnly=$(echo "${IS_TRAINING_POD_ONLY}" | tr '[:upper:]' '[:lower:]')

# Default arguments for launching WebUI API
defaultWebUIArgs="--api --nowebui --port 3000 --no-half --disable-nan-check --precision full --xformers"

# Use the WEBUI_API_ARGS environment variable if set, otherwise use the default
webUIArgs="${WEBUI_API_ARGS:-$defaultWebUIArgs}"

# Launch WebUI only if isTrainingPodOnly is unset, empty, or set to 'false'
if [ -z "${isTrainingPodOnly}" ] || [ "${isTrainingPodOnly}" = "false" ]; then
    echo "Starting WebUI API"
    source /venv/stable-diffusion-webui/venv/bin/activate
    python3.10 /workspace/stable-diffusion-webui/webui.py $webUIArgs > /workspace/logs/webui-api-${RUNPOD_POD_ID}.log 2>&1 &
    deactivate
else
    echo "Skipping WebUI API Launch as IS_TRAINING_POD_ONLY is set to true or TRUE"
fi

echo "Starting RunPod Handler"
python3 -u /rp_handler.py