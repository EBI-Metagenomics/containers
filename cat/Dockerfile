FROM ubuntu:20.04

ARG catVersion="5.2.3"
ARG diamondVer="2.0.6"
ARG prodigalVer="2.6.3"

LABEL software="CAT"
LABEL software.version="${catVersion}"
LABEL description="Contig Annotation Tool (CAT) and Bin Annotation Tool (BAT) are pipelines for the taxonomic classification of long DNA sequences and metagenome assembled genomes (MAGs/bins) "
LABEL website="https://github.com/dutilh/CAT"
LABEL license="https://github.com/dutilh/CAT/blob/master/LICENSE.md"

# install deps
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3 \
        wget


# install deps
WORKDIR /usr/local/bin

# install Diamond binary
RUN wget -q https://github.com/bbuchfink/diamond/releases/download/v${diamondVer}/diamond-linux64.tar.gz \
    && tar zxf diamond-linux64.tar.gz \
    && rm diamond-linux64.tar.gz \
    && chmod a+x diamond

# install Prodigal binary
RUN wget -q -O prodigal https://github.com/hyattpd/Prodigal/releases/download/v${prodigalVer}/prodigal.linux \
    && chmod a+x prodigal

# install CAT
WORKDIR /opt
RUN  wget -q https://github.com/dutilh/CAT/archive/refs/tags/v${catVersion}.tar.gz \
    && tar zxf v${catVersion}.tar.gz \
    && rm v${catVersion}.tar.gz

ENV PATH=$PATH:/opt/CAT-${catVersion}/CAT_pack/

# mount location for database
RUN mkdir /db

# setting workdir
RUN mkdir /data
WORKDIR /data

# for singularity compatibility
ENV LC_ALL=C

# simple executor
CMD ["/bin/bash", "-c"]