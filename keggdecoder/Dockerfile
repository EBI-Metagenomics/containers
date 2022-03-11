FROM ubuntu:20.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="1.3"
LABEL software="KEGGDecoder"
LABEL website="https://github.com/bjtully/BioData/tree/master/KEGGDecoder"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
RUN pip3 install --upgrade pip && \
    pip3 install KEGGDecoder

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
