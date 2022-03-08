FROM ubuntu:20.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="2.0"
LABEL software="genome-properties"
LABEL website="https://github.com/ebi-pf-team/genome-properties"
LABEL license="https://github.com/ebi-pf-team/genome-properties/blob/master/LICENSE"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        git \
        libwww-perl \
        libdata-printer-perl \
        libjson-perl \
        libclone-perl \
        liblog-log4perl-perl \
        libdbix-class-perl \
        libfile-slurp-perl \
    && rm -rf /var/lib/apt/lists/*

# Downloading source code and help files
WORKDIR /opt
RUN git clone https://github.com/ebi-pf-team/genome-properties.git
RUN chmod -R a+x /opt/genome-properties/code/scripts/*.pl
ENV PERL5LIB=/opt/genome-properties/code/modules
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/genome-properties/code/scripts/

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
