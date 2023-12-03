# Base image
FROM python:3.10-slim-buster

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
RUN accelerate config --num_processes 4 --num_machines 1 --mixed_precision yes --dynamo_backend yes


# Add src files
ADD src .
RUN ln -s /runpod-volume /workspace


# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD /start.sh
