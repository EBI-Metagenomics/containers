# Docker container for BWA and metabat2

FROM ubuntu:20.04

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        build-essential \
        samtools \
        wget \
        bzip2 \
        cmake \
        git \
        libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# install bwamem2
WORKDIR /tmp
ENV bwamem2Ver=2.2.1
RUN wget -q https://github.com/bwa-mem2/bwa-mem2/releases/download/v${bwamem2Ver}/bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    tar jxf bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    mv bwa-mem2-${bwamem2Ver}_x64-linux/bwa-mem2* /usr/local/bin/ && \
    rm -rf bwa-mem2-${bwamem2Ver}_x64-linux*

# metabat2
RUN wget https://bitbucket.org/berkeleylab/metabat/get/master.tar.gz \
    && tar xzvf master.tar.gz \
    && mv berkeleylab-metabat-* /usr/local/bin/ \
    && cd /usr/local/bin/berkeleylab-metabat-* \
    && mkdir -p build \
    && cd build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/bin \
    && make \
    && make test \
    && make install

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
