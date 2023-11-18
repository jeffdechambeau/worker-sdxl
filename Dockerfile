# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
# Base image
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Use bash shell with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set the working directory
WORKDIR /

# Update and upgrade the system packages (Worker Template)
COPY builder/setup.sh /setup.sh
RUN /bin/bash /setup.sh && \
    rm /setup.sh

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt && \
    rm /requirements.txt

# Cleanup section (Worker Template)
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Remove the empty workspace directory, link to runpod network volume
#RUN rm -rf /workspace && \ 
#ln -s /runpod-volume /workspace

ADD src .
RUN chmod a+x /start.sh
CMD /start.sh