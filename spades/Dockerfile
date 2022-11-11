# Docker container for SPAdes
FROM python:3.7.9-slim-buster

ARG spadesVer=3.15.3

LABEL software="SPAdes"
LABEL software.version="${spadesVer}"
LABEL description="SPAdes – St. Petersburg genome assembler – is an assembly toolkit containing various assembly pipelines"
LABEL website="https://github.com/ablab/spades"
LABEL license="GPLv2"

# install dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        wget && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

# install SPAdes
WORKDIR /opt
RUN wget -q https://github.com/ablab/spades/releases/download/v${spadesVer}/SPAdes-${spadesVer}-Linux.tar.gz && \
    tar zxf SPAdes-${spadesVer}-Linux.tar.gz && \
    rm SPAdes-${spadesVer}-Linux.tar.gz && \
    ln -s /opt/SPAdes-${spadesVer}-Linux/bin/* /usr/local/bin

RUN chmod +x /usr/local/bin/

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]