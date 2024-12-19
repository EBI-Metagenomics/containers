FROM python:3.10-slim

LABEL software="pseudofinder"
LABEL software.version="1.1.0"
LABEL website="https://github.com/filip-husnik/pseudofinder"
LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

ARG pseudofinderVer=1.1.0

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libncurses5-dev \
    libncursesw5-dev \
    zlib1g-dev \
    curl \
    parallel \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    biopython==1.79 \
    plotly==5.6.0 \
    pandas==1.4.1 \
    numpy==1.22.2 \
    reportlab==3.5.68

# Install BLAST
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/ncbi-blast-2.12.0+-x64-linux.tar.gz && \
    tar -xzf ncbi-blast-2.12.0+-x64-linux.tar.gz && \
    mv ncbi-blast-2.12.0+ /opt/blast && \
    ln -s /opt/blast/bin/* /usr/local/bin/ && \
    rm ncbi-blast-2.12.0+-x64-linux.tar.gz

# Install DIAMOND
RUN wget https://github.com/bbuchfink/diamond/releases/download/v2.0.14/diamond-linux64.tar.gz && \
    tar -xzf diamond-linux64.tar.gz && \
    mv diamond /usr/local/bin/ && \
    rm diamond-linux64.tar.gz

# Install PAL2NAL
RUN wget https://github.com/liaochenlanruo/PAL2NAL/archive/refs/tags/v14.1.tar.gz && \
    tar -xzf v14.1.tar.gz && \
    mv PAL2NAL-14.1 /opt/pal2nal && \
    chmod +x /opt/pal2nal/pal2nal.pl && \
    ln -s /opt/pal2nal/pal2nal.pl /usr/local/bin/pal2nal && \
    rm v14.1.tar.gz

# Install PAML
RUN wget https://github.com/abacus-gene/paml/archive/refs/tags/4.10.7.tar.gz && \
    tar -xzf 4.10.7.tar.gz && \
    mv paml-4.10.7 /opt/paml && \
    make -C /opt/paml/src && \
    ln -s /opt/paml/bin/* /usr/local/bin/ && \
    rm 4.10.7.tar.gz

# Install HMMER
RUN wget http://eddylab.org/software/hmmer/hmmer-3.2.1.tar.gz && \
    tar -xzf hmmer-3.2.1.tar.gz && \
    cd hmmer-3.2.1 && \
    ./configure && make && make install && \
    cd .. && rm -rf hmmer-3.2.1.tar.gz hmmer-3.2.1

# Install MUSCLE
RUN wget https://drive5.com/muscle/muscle_src_3.8.1551.tar.gz && \
    tar --one-top-level=muscle3.8.1551 -xzf muscle_src_3.8.1551.tar.gz && \
    mv muscle3.8.1551 /usr/local/bin/muscle && \
    rm muscle_src_3.8.1551.tar.gz

# Install Prodigal
RUN wget https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux && \
    mv prodigal.linux /usr/local/bin/prodigal && \
    chmod +x /usr/local/bin/prodigal

WORKDIR /opt
RUN wget https://github.com/filip-husnik/pseudofinder/archive/refs/tags/v1.1.0.tar.gz && \
    tar -xzf v1.1.0.tar.gz && \
    chmod u+x pseudofinder-1.1.0/pseudofinder.py && \
    rm v1.1.0.tar.gz

# for singularity compatibility
ENV LC_ALL=C

# Set working directory
RUN mkdir /data
WORKDIR /data

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/pseudofinder-1.1.0

# simple executor
CMD ["/bin/bash", "-c"]

