# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Use bash shell with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set the working directory
WORKDIR /

# Update and install dependencies
COPY builder/setup.sh /setup.sh
COPY builder/requirements.txt /requirements.txt
RUN /bin/bash /setup.sh && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /setup.sh /requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Symlink for workspace
RUN ln -s /runpod-volume /workspace

# Add src files
ADD src .

# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD ["/start.sh"]
