FROM ubuntu:20.04

ARG HiFiVer=3.0.0
ARG blastVer=2.12.0

LABEL software="HiFiAdapterFilt"
LABEL software.version="${HiFiVer}"
LABEL description="Convert .bam to .fastq and remove reads with remnant PacBio adapter sequences"
LABEL website="https://github.com/sheinasim/HiFiAdapterFilt"
LABEL license="GPLv2"

ENV DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt update \
    && apt install -q -y --no-install-recommends \
            ca-certificates \
            original-awk \
            dateutils \
            procps \
            pcregrep \
            sed \
            wget \
            git \
            bamtools \
    && rm -rf /var/lib/apt/lists/*

# install blast
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/${blastVer}/ncbi-blast-${blastVer}+-x64-linux.tar.gz && \
    tar -xzf ncbi-blast-${blastVer}+-x64-linux.tar.gz && \
    rm ncbi-blast-${blastVer}+-x64-linux.tar.gz

ENV PATH=/ncbi-blast-${blastVer}+/bin:$PATH

# install HiFiAdapterFilt
WORKDIR /opt
RUN git clone https://github.com/sheinasim/HiFiAdapterFilt.git

WORKDIR /opt/HiFiAdapterFilt

# for singularity compatibility
ENV LC_ALL=C

CMD ["/bin/bash", "-c"]