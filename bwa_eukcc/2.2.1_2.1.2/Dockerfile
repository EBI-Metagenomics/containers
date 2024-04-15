# Docker container for BWA and eukcc

FROM ubuntu:20.04

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        build-essential \
        samtools \
        wget \
        bzip2 \
        cmake \
        git \
        libboost-all-dev \
        original-awk \
        dateutils \
        procps \
        pcregrep \
        sed \
        python3-pip libgsl0-dev bedtools mummer \
    && pip3 install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# install bwamem2
WORKDIR /tmp
ENV bwamem2Ver=2.2.1
RUN wget -q https://github.com/bwa-mem2/bwa-mem2/releases/download/v${bwamem2Ver}/bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    tar jxf bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    mv bwa-mem2-${bwamem2Ver}_x64-linux/bwa-mem2* /usr/local/bin/ && \
    rm -rf bwa-mem2-${bwamem2Ver}_x64-linux*

ENV eukccVer=2.1
RUN wget https://github.com/EBI-Metagenomics/EukCC/archive/refs/tags/v.${eukccVer}.tar.gz \
    && tar xzvf v.${eukccVer}.tar.gz \
    && cd EukCC-v.${eukccVer} \
    && python3 setup.py sdist bdist_wheel \
    && pip3 install -e .


RUN mkdir /data
WORKDIR /data

# for singularity compatibility
ENV LC_ALL=C

COPY ggp_binlinks.py /usr/local/bin/
RUN chmod +x /usr/local/bin/ggp_binlinks.py

# simple executor
CMD ["/bin/bash", "-c"]
