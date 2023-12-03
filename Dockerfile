# Base image
FROM python:3.10-slim-buster
#FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Set the working directory
WORKDIR /

# Install System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    git \
    wget \
    openssh-server \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && rm /requirements.txt
#COPY builder/accelerate.yaml /accelerate.yaml
COPY builder/accelerate.yaml  ~/.cache/huggingface/accelerate/default_config.yaml
#RUN accelerate config --config_file accelerate.yaml
 


# Add src files
ADD src .
RUN ln -s /runpod-volume /workspace


# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD /start.sh
