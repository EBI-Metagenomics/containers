# Dockerfile for merge_reads

FROM ubuntu:20.04

LABEL software="Merge Reads"
LABEL software.version="1.0.0"
LABEL description="This is a simple tool to merge paired-end Fastq files."

# update/upgrade
RUN apt update && \
    apt upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# main script
COPY merge_reads.pl /usr/local/bin/
RUN chmod +x /usr/local/bin/merge_reads.pl

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
