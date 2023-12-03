# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Environment settings
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Use bash shell with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set the working directory
WORKDIR /

# Copy setup script and requirements
COPY builder/setup.sh /setup.sh
COPY builder/requirements.txt /requirements.txt

# Run setup script
RUN /bin/bash /setup.sh && rm /setup.sh

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r /requirements.txt && rm /requirements.txt

# Link to runpod volume
RUN ln -s /runpod-volume /workspace

# Add src files
ADD src .

# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD /start.sh
