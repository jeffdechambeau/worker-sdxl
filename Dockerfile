FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 as base
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Seattle \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

RUN echo "Update Apt-Get & Install system deps" && \
    apt update && apt -y upgrade && \
    apt install -y --no-install-recommends \
        build-essential software-properties-common python3.10-venv python3-pip python3-tk python3-dev nodejs npm \
        bash dos2unix git git-lfs ncdu nginx net-tools inetutils-ping openssh-server libglib2.0-0 libsm6 libgl1 \
        libxrender1 libxext6 ffmpeg wget curl psmisc rsync vim zip unzip p7zip-full htop pkg-config plocate \
        libcairo2-dev libgoogle-perftools4 libtcmalloc-minimal4 apt-transport-https ca-certificates && \
    update-ca-certificates && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

RUN ln -s /usr/bin/python3.10 /usr/bin/python

FROM base as setup
RUN echo "Installing core ML cuda jazz"

RUN pip3 install --no-cache-dir torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchmetrics==0.11.4 --extra-index-url https://download.pytorch.org/whl/cu118 # no_verify leave this to specify not checking this a verification stage && \
    pip3 install --no-cache-dir xformers==0.0.22 tensorrt && pytorch-lightning==1.8.*  open-clip-torch==2.18.0 && \ 
    pip3 install --no-cache-dir torchdiffeq torchsde transformers && \
    pip3 cache purge

#RUN echo "Installing requirements.txt"
#COPY builder/* . 
#RUN pip3 --no-cache-dir install -r requirements.txt && \ pip3 cache purge

WORKDIR /
RUN echo "Installing stable-diffusion-webui and A1111 Extensions" && \
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /stable-diffusion-webui && \
    cd /stable-diffusion-webui && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements.txt && \
    git clone --depth=1 https://github.com/Bing-su/adetailer.git extensions/adetailer && \
    git clone --depth=1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    pip3 install -r extensions/sd-webui-controlnet/requirements.txt && \
    cd extensions/adetailer && \
    pip3 install . && \
    pip3 install segment_anything lama_cleaner && \
    pip3 cache purge && \
    deactivate

RUN echo "Installing Kohya_ss" && \
    git clone https://github.com/bmaltais/kohya_ss.git && \
    cd kohya_ss && \
    python3 -m venv --system-site-packages venv && \
    source venv/bin/activate && \
    pip3 install --no-cache-dir -r requirements-runpod.txt && \
    pip3 install . && \
    pip3 cache purge && \
    deactivate

RUN echo "Installing misc extras" && \
    wget https://github.com/runpod/runpodctl/releases/download/v1.10.0/runpodctl-linux-amd -O runpodctl && \
    chmod a+x runpodctl && \
    mv runpodctl /usr/local/bin

ADD https://raw.githubusercontent.com/Douleb/SDXL-750-Styles-GPT4-/main/styles.csv /workspace/stable-diffusion-webui/styles.csv

RUN echo "Fixing Tensorboard" && \
    pip3 uninstall -y tensorboard tb-nightly && \
    pip3 install tensorboard tensorflow && \
    pip3 cache purge 


COPY src .
RUN ln -s /runpod-volume /workspace && \
    chmod +x /start.sh

SHELL ["/bin/bash", "--login", "-c"]
CMD ["/start.sh"]
