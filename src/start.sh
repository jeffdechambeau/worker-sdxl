#!/bin/bash

echo "Entering /start.sh"

# For some reason, pod cloud env doesn't look for packages here, which is where runpod module is
# so the first addition is to make the env in cloud aware of local dist-packages
# the second addition is to make container aware of where modeules were installed on network volume
export PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.10/dist-packages:/workspace/venv/lib/python3.10/site-packages"

python3 --version
python3 -c "import sys; print(sys.path)"
pip --version
pip freeze

echo "Starting WebUI API"
python3 /workspace/stable-diffusion-webui/webui.py --skip-python-version-check --skip-torch-cuda-test --skip-install --lowram --opt-sdp-attention --disable-safe-unpickle --port 3000 --api --nowebui --skip-version-check  --no-hashing --no-download-sd-model &

echo "Starting RunPod Handler"
python3 -u /handler.py