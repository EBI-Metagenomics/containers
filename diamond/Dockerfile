# Dockerfile for DIAMOND
FROM ubuntu:20.04

LABEL software="DIAMOND"
LABEL software.version="2.0.12"
LABEL description="DIAMOND is a sequence aligner for protein and translated DNA searches, designed for high performance analysis of big sequence data"
LABEL website="https://github.com/bbuchfink/diamond"
LABEL license="https://github.com/bbuchfink/diamond/blob/master/LICENSE"


# install deps
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y wget

# install diamond binary
WORKDIR /usr/local/bin
ENV diamondVer=2.0.12
RUN wget -q https://github.com/bbuchfink/diamond/releases/download/v${diamondVer}/diamond-linux64.tar.gz \
    && tar zxf diamond-linux64.tar.gz \
    && rm diamond-linux64.tar.gz \
    && chmod a+x diamond

# setting workdir
RUN mkdir /data
WORKDIR /data

# for singularity compatibility
ENV LC_ALL=C

# simple executor
CMD ["/bin/bash", "-c"]