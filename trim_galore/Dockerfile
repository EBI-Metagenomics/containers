# Docker container for TrimGalore

FROM ubuntu:latest

LABEL software="TrimGalore"
LABEL software.version="0.6.7"
LABEL description="Trim Galore is a wrapper around Cutadapt and FastQC to consistently apply adapter and quality trimming to FastQ files, with extra functionality for RRBS data."
LABEL website="https://github.com/FelixKrueger/TrimGalore"
LABEL license="GPLv3"

# Deps
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        build-essential \
        curl \
        default-jre \
        git \
        python3 \
        python3-dev \
        python3-pip

# Install cutadapt
WORKDIR /opt
RUN pip3 install --upgrade cutadapt

# Install fastqc
WORKDIR /opt
RUN git clone https://github.com/s-andrews/FastQC.git && \
    chmod 755 FastQC/fastqc

ENV PATH="/opt/FastQC/fastqc:/opt/FastQC:${PATH}"

# Install TrimGalore
WORKDIR /opt
RUN curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.7.tar.gz -o trim_galore_0.6.7.tar.gz && \
    tar xvzf trim_galore_0.6.7.tar.gz

ENV PATH="/opt/trim_galore_0.6.7/trim_galore:/opt/trim_galore_0.6.7:${PATH}"

# Entrypoint
ENTRYPOINT ["/bin/bash", "-c"]
CMD trim_galore