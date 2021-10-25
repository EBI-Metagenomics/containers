# Dockerfile for filterContigs
FROM ubuntu:20.04

LABEL software="filterContigs"
LABEL software.version="1.0.0"
LABEL description="Quick tool to filter contigs by size from a Fasta input"
LABEL website="https://github.com/EBI-Metagenomics/mgnify-lr"
LABEL license="https://github.com/EBI-Metagenomics/mgnify-lr/blob/master/LICENSE"

# update base image
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# main scripts
COPY filterContigs.pl /usr/local/bin
RUN chmod +x /usr/local/bin/filterContigs.pl

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]