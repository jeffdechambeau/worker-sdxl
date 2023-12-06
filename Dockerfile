FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /



RUN apt update && \
    apt install -y --no-install-recommends \
        build-essential software-properties-common python3-pip python3.10-venv \
        git wget curl vim zip unzip \
        libgl1 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

FROM base as setup

RUN ln -s /usr/bin/python3.10 /usr/bin/python


RUN echo "Installing Kohya_ss" && \
    git clone https://github.com/bmaltais/kohya_ss.git /kohya_ss && \
    cd /kohya_ss && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install opencv-python bitsandbytes scipy && \
    pip3 install . && \
    pip3 cache purge && \
    

RUN echo "Installing A1111" && \
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /stable-diffusion-webui && \
    cd /stable-diffusion-webui && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 cache purge && \
    deactivate

RUN echo "Installing Adetailer" && \
    cd /stable-diffusion-webui && \
    source venv/bin/activate && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \ 
    cd /stable-diffusion-webui/extensions/adetailer && \
    pip3 install . && \
    pip3 install segment_anything lama_cleaner && \
    pip3 cache purge && \
    deactivate

RUN echo "Installing ControlNet" && \
    cd /stable-diffusion-webui && \
    source venv/bin/activate && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    pip3 install -r extensions/sd-webui-controlnet/requirements.txt && \
    pip3 cache purge && \
    deactivate

RUN echo "Installing misc extras" && \
    wget https://github.com/runpod/runpodctl/releases/download/v1.10.0/runpodctl-linux-amd -O runpodctl && \
    chmod a+x runpodctl && \
    mv runpodctl /usr/local/bin

ADD https://civitai.com/api/download/models/131579?type=Model&format=SafeTensor&size=full&fp=fp16 /stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors
# ADD https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors /stable-diffusion-webui/models/VAE/sdxl_vae.safetensors
ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /stable-diffusion-webui/styles.csv

COPY src .

RUN source /venv/bin/activate && \
    pip3 install runpod && \
    ln -s /runpod-volume /workspace && \
    chmod +x /start.sh

SHELL ["/bin/bash", "--login", "-c"]
CMD ["/start.sh"]
