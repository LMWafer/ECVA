FROM ubuntu:20.04

CMD [ "python3", "main.py" ]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -qq --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
        python3 \
        python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install opencv-python pyrealsense2 && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY . .