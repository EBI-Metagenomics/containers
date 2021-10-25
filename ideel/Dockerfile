# Docker contained for Ideel
FROM ubuntu:20.04

LABEL software="ideel"
LABEL software.version="1.0.0"
LABEL description="ideel is histogram report for mgnify-lr"
LABEL website="https://github.com/EBI-Metagenomics/mgnify-lr"
LABEL license="https://github.com/EBI-Metagenomics/mgnify-lr/blob/master/LICENSE"

# install deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# main script
COPY ideel.py /usr/local/bin/
RUN chmod +x /usr/local/bin/ideel.py

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]