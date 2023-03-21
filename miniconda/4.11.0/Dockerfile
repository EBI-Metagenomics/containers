FROM ubuntu:20.04

ARG minicondaVer=4.11.0

LABEL software="miniconda"
LABEL software.version=${minicondaVer}
LABEL description="Miniconda base image to install BioConda recipes"
LABEL website="https://docs.conda.io/en/latest/miniconda.html"
LABEL license="https://www.anaconda.com/end-user-license-agreement-miniconda"


ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        wget && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

# Installing miniconda
WORKDIR /opt
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-py39_${minicondaVer}-Linux-x86_64.sh && \
    bash Miniconda3-py39_${minicondaVer}-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-py39_${minicondaVer}-Linux-x86_64.sh && \
    chmod a+x /opt/miniconda/bin/*
ENV PATH /opt/miniconda/bin:$PATH

# add mamba 
RUN conda install -c conda-forge -y mamba

# conda clenup
RUN conda clean -y -a

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
