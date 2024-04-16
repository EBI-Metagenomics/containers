# Docker container for BWA, metabat2 and concoct

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
        tabix \
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

# CONCOCT
ENV concoctVer=1.1.0
RUN wget https://github.com/BinPro/CONCOCT/archive/refs/tags/${concoctVer}.tar.gz \
    && tar xzvf ${concoctVer}.tar.gz \
    && cd CONCOCT-${concoctVer} \
    && pip3 install -r requirements.txt \
    && python3 setup.py install \
    && rm -rf ${concoctVer}.tar.gz

# metabat2 2.16
ENV metabatHash=1dc5822668165fb32bb4b608b0816b42dbfd20d0
RUN wget https://bitbucket.org/berkeleylab/metabat/get/${metabatHash}.tar.gz \
    && tar xzvf ${metabatHash}.tar.gz \
    && rm -rf ${metabatHash}.tar.gz \
    && mv berkeleylab-metabat-* /usr/local/bin \
    && cd /usr/local/bin/berkeleylab-metabat-* \
    && mkdir -p build \
    && cd build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/bin \
    && make \
    && make test \
    && make install

# for singularity compatibility
ENV LC_ALL=C
ENV PATH=/usr/local/bin/bin:$PATH
# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]