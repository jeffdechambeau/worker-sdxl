FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev python3-pip python3.10-venv libopencv-dev \
    git wget curl vim zip unzip libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting up Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Clone and setup all repositories and dependencies
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /stable-diffusion-webui && \
    git clone https://github.com/bmaltais/kohya_ss.git /kohya_ss && \
    cd /stable-diffusion-webui && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install xformers && \
    pip3 cache purge && \
    deactivate && \
    cd /kohya_ss && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install runpod opencv-python bitsandbytes scipy && \
    pip3 install . && \
    pip3 cache purge

# Download models and styles at runtime or use a separate script to reduce image size
# ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /stable-diffusion-webui/styles.csv

COPY src /src
COPY builder /builder
COPY start.sh /start.sh

RUN chmod +x /start.sh

WORKDIR /
CMD ["/start.sh"]
