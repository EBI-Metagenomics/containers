FROM ubuntu:24.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:24.04"
LABEL software="MAPseq"
LABEL software.version="v2.1.1b"
LABEL about.license="SPDX:GPL-3.0"
LABEL about.home="https://github.com/meringlab/MAPseq"

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        dateutils \
        procps \
        pcregrep \
        sed \
        wget \
    && rm -rf /var/lib/apt/lists/*

ENV MAPSEQ_VERSION="2.1.1b"

WORKDIR /opt/mapseq
RUN wget -q https://github.com/meringlab/MAPseq/releases/download/v${MAPSEQ_VERSION}/mapseq-${MAPSEQ_VERSION}.tar.gz && \
    tar -xvzf mapseq-${MAPSEQ_VERSION}.tar.gz && \
    mv build/bin/mapseq /usr/local/bin/ && \
    rm -rf build && rm mapseq-${MAPSEQ_VERSION}.tar.gz

ENV LC_ALL=C

CMD ["/bin/bash", "-c"]
