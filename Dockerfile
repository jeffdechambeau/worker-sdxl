# Stage 1: Base
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 as base

ARG WEBUI_VERSION=v1.6.0
ARG DREAMBOOTH_COMMIT=cf086c536b141fc522ff11f6cffc8b7b12da04b9
ARG KOHYA_VERSION=v22.2.1

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle\
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Create workspace working directory
WORKDIR /

# Install Ubuntu packages
RUN apt update && apt -y upgrade && apt install -y --no-install-recommends \
        build-essential software-properties-common python3.10-venv python3-pip python3-tk python3-dev nodejs npm \
        bash dos2unix git git-lfs ncdu nginx net-tools inetutils-ping openssh-server libglib2.0-0 libsm6 libgl1 \
        libxrender1 libxext6 ffmpeg wget curl psmisc rsync vim zip unzip p7zip-full htop pkg-config plocate \
        libcairo2-dev libgoogle-perftools4 libtcmalloc-minimal4 apt-transport-https ca-certificates && \
    update-ca-certificates && apt clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# Set Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Install Torch, xformers, and tensorrt
RUN pip3 install --no-cache-dir torch==2.0.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install --no-cache-dir xformers==0.0.22 tensorrt && \
    pip3 install runpod && \
    pip3 install accelerate pytorch_lightning diffusers omegaconf transformers kornia && \
    pip3 install toml gradio einops && \
    pip3 cache purge


# Stage 2: Install applications
FROM base as setup

WORKDIR /
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git && \
    cd /stable-diffusion-webui && \
    git checkout tags/${WEBUI_VERSION}

WORKDIR /stable-diffusion-webui
RUN python3 -m venv --system-site-packages /venv && \
    source /venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    deactivate

# Clone the Automatic1111 Extensions
RUN git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet

RUN source /venv/bin/activate && \
    cd /stable-diffusion-webui/extensions/sd-webui-controlnet && \
    pip3 install -r requirements.txt && \
    cd /stable-diffusion-webui/extensions/adetailer && \
    pip3 install . && \
    pip3 install segment_anything lama_cleaner && \
    deactivate

# Add inswapper model for the ReActor extension
RUN mkdir -p /stable-diffusion-webui/models/insightface && \
    cd /stable-diffusion-webui/models/insightface && \
    wget https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx

# Fix Tensorboard
RUN source /venv/bin/activate && \
    pip3 uninstall -y tensorboard tb-nightly && \
    pip3 install tensorboard tensorflow && \
    pip3 cache purge && \
    deactivate

# Install Kohya_ss
RUN git clone https://github.com/bmaltais/kohya_ss.git /kohya_ss
WORKDIR /kohya_ss
RUN git checkout ${KOHYA_VERSION} && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    # If the requirements.txt file is in the kohya_ss repository, it will be used here.
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install . && \
    pip3 cache purge && \
    deactivate
# Install Application Manager
WORKDIR /
RUN git clone https://github.com/ashleykleynhans/app-manager.git /app-manager && \
    cd /app-manager && \
    npm install

# Install rclone
RUN curl https://rclone.org/install.sh | bash

# Install runpodctl
RUN wget https://github.com/runpod/runpodctl/releases/download/v1.10.0/runpodctl-linux-amd -O runpodctl && \
    chmod a+x runpodctl && \
    mv runpodctl /usr/local/bin

# Install croc
RUN curl https://getcroc.schollz.com | bash

# Install speedtest CLI
RUN curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash && \
    apt install speedtest

# ADD SDXL styles.csv
ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /stable-diffusion-webui/styles.csv

WORKDIR /

COPY builder/accelerate.yaml ./

RUN ln -s /runpod-volume /workspace

COPY src .

RUN chmod +x /start.sh

# Start the container
SHELL ["/bin/bash", "--login", "-c"]
CMD ["/start.sh"]
