# Docker container for TrimGalore

FROM ubuntu:22.04

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
        curl \
        default-jre \
        python3 \
        python3-pip \
        unzip \
        wget

# Install cutadapt
WORKDIR /opt
RUN pip3 install --upgrade cutadapt==4.0

# Install fastqc
WORKDIR /opt
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && \
    unzip fastqc_v0.11.9.zip && \
    rm fastqc_v0.11.9.zip && \
    chmod 755 FastQC/fastqc

ENV PATH="/opt/FastQC:${PATH}"

# Install TrimGalore
WORKDIR /opt
RUN curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.7.tar.gz -o trim_galore_0.6.7.tar.gz && \
    tar xvzf trim_galore_0.6.7.tar.gz && \
    rm trim_galore_0.6.7.tar.gz

ENV PATH="/opt/TrimGalore-0.6.7:${PATH}"

# for singularity compatibility
ENV LC_ALL=C

CMD ["/bin/bash", "-c"]