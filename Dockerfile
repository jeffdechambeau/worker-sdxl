FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev python3-pip python3.10-venv libopencv-dev \
    git wget curl vim zip unzip libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setting up Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Clone A1111 and Kohya_ss repositories
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /stable-diffusion-webui && \
    git clone https://github.com/bmaltais/kohya_ss.git /kohya_ss

# Setup Stable Diffusion WebUI (A1111)
WORKDIR /stable-diffusion-webui
COPY builder .
RUN python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt xformers && \
    pip3 cache purge

# Run install-automatic.py with cleanup
RUN source venv/bin/activate && \
    python3 install-automatic.py --skip-torch-cuda-test && \
    pip3 cache purge && \
    deactivate && \
    rm -rf /root/.cache/pip

# Install Adetailer extension with cleanup
RUN source venv/bin/activate && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    cd extensions/adetailer && pip3 install . segment_anything lama_cleaner && \
    pip3 cache purge && \
    deactivate && \
    rm -rf /root/.cache/pip

# Install ControlNet extension with cleanup
RUN source venv/bin/activate && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    cd extensions/sd-webui-controlnet && pip3 install -r requirements.txt && \
    pip3 cache purge && \
    deactivate && \
    rm -rf /root/.cache/pip

# Setup Kohya_ss with cleanup
WORKDIR /kohya_ss
RUN pip3 install --no-cache-dir -r requirements.txt runpod opencv-python bitsandbytes scipy && \
    pip3 install . && \
    pip3 cache purge && \
    rm -rf /root/.cache/pip

# Prepare runtime environment
COPY src /
RUN chmod +x /start.sh
RUN ln -s /runpod-volume /workspace

WORKDIR /
CMD ["/start.sh"]
