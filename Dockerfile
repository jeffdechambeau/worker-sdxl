# Stage 1: Base
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 as base

ARG WEBUI_VERSION=v1.6.0
ARG DREAMBOOTH_COMMIT=cf086c536b141fc522ff11f6cffc8b7b12da04b9
ARG KOHYA_VERSION=v22.2.1

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Create workspace working directory
WORKDIR /

# Install Ubuntu packages
RUN apt update && apt -y upgrade && \
    apt install -y --no-install-recommends \
        build-essential software-properties-common python3.10-venv python3-pip python3-tk python3-dev nodejs npm \
        bash dos2unix git git-lfs ncdu nginx net-tools inetutils-ping openssh-server libglib2.0-0 libsm6 libgl1 \
        libxrender1 libxext6 ffmpeg wget curl psmisc rsync vim zip unzip p7zip-full htop pkg-config plocate \
        libcairo2-dev libgoogle-perftools4 libtcmalloc-minimal4 apt-transport-https ca-certificates && \
    update-ca-certificates && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# Set Python and Symlink for workspace
RUN ln -s /usr/bin/python3.10 /usr/bin/python && \
    ln -s /runpod-volume /workspace

# Stage 2: Install applications
FROM base as setup

# Install Torch, xformers and tensorrt
RUN pip3 install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchmetrics==0.11.4 --extra-index-url https://download.pytorch.org/whl/cu118 # no_verify leave this to specify not checking this a verification stage && \
    pip3 install --no-cache-dir xformers==0.0.22 tensorrt && pytorch-lightning==1.8.*  open-clip-torch==2.18.0 && \ 
    pip4 install --no-cache-dir torchdiffeq torchsde transformers && \
    pip3 cache purge

# Install requirements
COPY builder/requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt && \
    pip3 cache purge

# Clone and set up stable-diffusion-webui
WORKDIR /stable-diffusion-webui
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git . && \
    git checkout tags/${WEBUI_VERSION} && \
    python3 -m venv --system-site-packages /venv && \
    source /venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    deactivate && \
    pip3 cache purge

# Clone the Automatic1111 Extensions
RUN git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet

# Install extensions and additional packages
RUN source /venv/bin/activate && \
    cd extensions/sd-webui-controlnet && \
    pip3 install -r requirements.txt && \
    cd ../../extensions/adetailer && \
    pip3 install . && \
    pip3 install segment_anything lama_cleaner && \
    deactivate && \
    pip3 cache purge

# Add inswapper model for the ReActor extension
RUN mkdir -p models/insightface && \
    cd models/insightface && \
    wget https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx

# Fix Tensorboard
RUN source /venv/bin/activate && \
    pip3 uninstall -y tensorboard tb-nightly && \
    pip3 install tensorboard tensorflow && \
    pip3 cache purge && \
    deactivate

# Install Kohya_ss
WORKDIR /kohya_ss
RUN git clone https://github.com/bmaltais/kohya_ss.git . && \
    git checkout ${KOHYA_VERSION} && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install . && \
    pip3 cache purge && \
    deactivate



# Additional installations
RUN curl https://rclone.org/install.sh | bash && \
    wget https://github.com/runpod/runpodctl/releases/download/v1.10.0/runpodctl-linux-amd -O runpodctl && \
    chmod a+x runpodctl && \
    mv runpodctl /usr/local/bin && \
    curl https://getcroc.schollz.com | bash

# ADD SDXL styles.csv
ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /stable-diffusion-webui/styles.csv

WORKDIR /

# Copy source files and set permissions
COPY src .
RUN chmod +x /start.sh

# Start the container
SHELL ["/bin/bash", "--login", "-c"]
CMD ["/start.sh"]
