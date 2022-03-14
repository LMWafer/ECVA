FROM adujardin/magicleap-atlas:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -qq --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install scikit-image && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/