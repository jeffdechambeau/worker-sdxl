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

# Clone and setup A1111 and Kohya_ss repositories and dependencies
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /stable-diffusion-webui && \
    git clone https://github.com/bmaltais/kohya_ss.git /kohya_ss

# Setup Stable Diffusion WebUI (A1111)
WORKDIR /stable-diffusion-webui
COPY builder .
RUN python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt xformers && \
    python3 install-automatic.py --skip-torch-cuda-test && \
    pip3 cache purge && \
    deactivate

# Install Adetailer and ControlNet extensions
RUN source venv/bin/activate && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    cd extensions/adetailer && pip3 install . segment_anything lama_cleaner && \
    cd ../sd-webui-controlnet && pip3 install -r requirements.txt && \
    pip3 cache purge && \
    deactivate

# Setup Kohya_ss
WORKDIR /kohya_ss
RUN pip3 install --no-cache-dir -r requirements.txt runpod opencv-python bitsandbytes scipy && \
    pip3 install . && \
    pip3 cache purge

# Download models and styles at runtime or use a separate script to reduce image size
# ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /stable-diffusion-webui/styles.csv

WORKDIR /
COPY src .  
RUN chmod +x /start.sh
CMD ["/start.sh"]
