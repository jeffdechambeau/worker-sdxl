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
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && rm /requirements.txt

# Add src files
ADD src .
RUN ln -s /runpod-volume /workspace


# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD /start.sh
