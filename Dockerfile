# Base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

COPY builder/requirements.txt /requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade -r /requirements.txt && \
    rm /requirements.txt

RUN ln -s /runpod-volume /workspace

ADD src .
RUN chmod a+x /start.sh
CMD /start.sh