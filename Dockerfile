FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install core dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev python3-pip python3.10-venv libopencv-dev git wget curl vim zip unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting up Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Create a virtual environment for stable-diffusion-webui
WORKDIR /venv/stable-diffusion-webui
RUN python3 -m venv --system-site-packages venv

# Clone and set up stable-diffusion-webui in its venv
WORKDIR /stable-diffusion-webui
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git . && \
    /venv/stable-diffusion-webui/venv/bin/pip install --no-cache-dir -r requirements.txt xformers && \
    /venv/stable-diffusion-webui/venv/bin/pip cache purge && \
    rm -rf /root/.cache/pip

# Install extensions (Adetailer, ControlNet, and API Payload Display)
COPY builder/install-automatic.py .
RUN source /venv/stable-diffusion-webui/venv/bin/activate && \
    python3 install-automatic.py --skip-torch-cuda-test && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    cd extensions/adetailer && pip install . segment_anything lama_cleaner && \
    cd /stable-diffusion-webui && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    pip install -r extensions/sd-webui-controlnet/requirements.txt && \
    git clone --depth=1 https://github.com/huchenlei/sd-webui-api-payload-display.git extensions/sd-webui-api-payload-display && \
    pip cache purge && \
    rm -rf /root/.cache/pip /root/.cache/huggingface_hub 

# Install system level deps (for kohya_ss and others)
RUN pip3 install requests runpod opencv-python bitsandbytes scipy accelerate && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip

# Clone and set up Kohya_ss at the Docker level
WORKDIR /kohya_ss
RUN git clone https://github.com/bmaltais/kohya_ss.git . && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install . && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip 

# Misc extras
WORKDIR /
COPY src/ /
COPY builder/accelerate.yaml /root/.cache/huggingface/accelerate/default_config.yaml

RUN ln -s /runpod-volume /workspace && \
    chmod +x setup.sh && \
    chmod +x start.sh 

CMD ["/start.sh"]
# We call setup.sh in startup.sh to
# optionally load assets to the network mount.
