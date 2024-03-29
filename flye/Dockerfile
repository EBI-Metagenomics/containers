# Docker container for Flye
FROM ubuntu:20.04 AS builder

ARG flyeVer=2.9

# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3 \
        python3-setuptools \
        build-essential \
        zlib1g-dev \
        wget && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

# install Flye
WORKDIR /opt
RUN wget -q https://github.com/fenderglass/Flye/archive/${flyeVer}.tar.gz && \
    tar zxf ${flyeVer}.tar.gz && \
    rm ${flyeVer}.tar.gz && \
    cd Flye-${flyeVer} && \
    make && \
    rm -rf src/

# Target container
FROM ubuntu:20.04

ARG flyeVer=2.9

LABEL software="Flye"
LABEL software.version=${flyeVer}
LABEL description="Flye is a de novo assembler for single molecule sequencing reads, such as those produced by PacBio and Oxford Nanopore Technologies."
LABEL website="https://github.com/fenderglass/Flye"
LABEL license="https://github.com/fenderglass/Flye/blob/flye/LICENSE"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3-minimal && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/Flye-${flyeVer} /opt/Flye-${flyeVer}
RUN ln -s /opt/Flye-${flyeVer}/bin/flye /usr/local/bin

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]