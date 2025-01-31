# Docker container for BWA and metabat2

FROM ubuntu:20.04

# install dependencies
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        build-essential \
        samtools \
        wget \
        bzip2 \
        cmake \
        git \
        libboost-program-options-dev \
        libboost-filesystem-dev \
        libboost-thread-dev \
        original-awk \
        dateutils \
        procps \
        pcregrep \
        sed \
    && rm -rf /var/lib/apt/lists/*

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

# Remove build tools after installation
RUN apt-get remove -y build-essential cmake git && apt-get autoremove -y

# install minimap2
ENV minimap2Ver=2.22
WORKDIR /opt
RUN wget https://github.com/lh3/minimap2/releases/download/v${minimap2Ver}/minimap2-${minimap2Ver}_x64-linux.tar.bz2 && \
    tar jxvf minimap2-${minimap2Ver}_x64-linux.tar.bz2 --no-same-owner && \
    cp minimap2-${minimap2Ver}_x64-linux/minimap2 /usr/local/bin && \
    rm -rf minimap2-${minimap2Ver}_x64-linux*

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]