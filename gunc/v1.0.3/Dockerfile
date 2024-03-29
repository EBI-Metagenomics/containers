FROM ubuntu:latest

LABEL software="GUNC"
LABEL software.version="1.0.3"
LABEL description="Genome UNClutterer (GUNC) is a tool for detection of chimerism and contamination in prokaryotic genomes resulting from mis-binning of genomic contigs from unrelated lineages"
LABEL website="https://github.com/grp-bork/gunc"
LABEL license="GPLv3"

RUN apt update && \
    apt-get install -q -y --no-install-recommends \
        python3 \
        python3-pip \
        wget \
        original-awk \
        dateutils \
        procps \
        pcregrep \
        sed \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/bin

# Install Diamond 2.0.4
ARG diamondVer=2.0.4
RUN wget https://github.com/bbuchfink/diamond/releases/download/v$diamondVer/diamond-linux64.tar.gz && \
    tar zxf diamond-linux64.tar.gz && \
    rm diamond-linux64.tar.gz

# Install Prodigal
ARG prodigalVer=2.6.3
RUN wget -O prodigal https://github.com/hyattpd/Prodigal/releases/download/v$prodigalVer/prodigal.linux && \
    chmod a+x prodigal

# Install GUNC
RUN pip3 install gunc==1.0.3

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/tools

# Entrypoint
CMD ["/bin/bash", "-c"]