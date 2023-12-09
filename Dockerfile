FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Important notes:

# These build steps are such so that
# this Dockerfile will build successfully 
# via github automations.

# If any one step, or the combined total, 
# gets too big, the entire build will fail. 

# Install core dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev python3-pip python3.10-venv libopencv-dev git wget curl vim zip unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting up Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Clone and set up A1111
WORKDIR /stable-diffusion-webui
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git . && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt xformers && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip

# Install extensions (Adetailer and ControlNet)
COPY builder/install-automatic.py .
RUN source venv/bin/activate && \
    python3 install-automatic.py --skip-torch-cuda-test && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    cd extensions/adetailer && pip3 install . segment_anything lama_cleaner && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    pip3 install -r extensions/sd-webui-controlnet/requirements.txt && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip /root/.cache/huggingface_hub && \
    deactivate

# Install system level deps
RUN pip3 install requests runpod opencv-python bitsandbytes scipy accelerate && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip

# Clone and set up Kohya_ss
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