# Dockerfile for AssemblyStats

FROM ubuntu:21.04

LABEL software="AssemblyStats"
LABEL software.version="1.0.0"
LABEL description="Tools to compute assembly statistics (N50, coverage, contigs, ...)"
LABEL website="https://github.com/EBI-Metagenomics/mgnify-lr"
LABEL license="https://github.com/EBI-Metagenomics/mgnify-lr/blob/master/LICENSE"

# Install deps
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        wget \
        samtools \
        bzip2 \
    && rm -rf /var/lib/apt/lists/*

# get minimap2
ENV minimap2Ver=2.21
WORKDIR /opt
RUN wget -q https://github.com/lh3/minimap2/releases/download/v${minimap2Ver}/minimap2-${minimap2Ver}_x64-linux.tar.bz2 && \
    tar jxf minimap2-${minimap2Ver}_x64-linux.tar.bz2 && \
    cp minimap2-${minimap2Ver}_x64-linux/minimap2 /usr/local/bin && \
    rm -rf minimap2-${minimap2Ver}_x64-linux*

# aux scripts
COPY calc_stats.pl /usr/local/bin/
COPY gen_stats_json.pl /usr/local/bin/
RUN chmod +x /usr/local/bin/*

# for singularity compatibility
ENV LC_ALL=C

# setting a workdir
RUN mkdir /data
WORKDIR /data

# simple exec
CMD ["/bin/bash", "-c"]