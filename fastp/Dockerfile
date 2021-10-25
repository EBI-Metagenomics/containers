# Dockerfile for fastp

FROM ubuntu:20.04

ENV fastpVer=0.23.1
LABEL software="fastp"
LABEL software.version="$fastpVer"
LABEL description="A tool designed to provide fast all-in-one preprocessing for FastQ files."
LABEL website="https://github.com/OpenGene/fastp"
LABEL license="https://github.com/OpenGene/fastp/blob/master/LICENSE"

# adding bash for compatibility
RUN apt update \
    && apt upgrade -y \
    && apt install -y wget

# install fastp
WORKDIR /usr/local/bin
RUN wget -q -O fastp 'http://opengene.org/fastp/fastp.${fastpVer}' && \
    chmod a+x fastp

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple exec
CMD ["/bin/bash", "-c"]