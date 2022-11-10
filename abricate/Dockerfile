FROM ubuntu:20.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="1.0.0"
LABEL software="abricate"
LABEL website="https://github.com/tseemann/abricate"
LABEL license="https://github.com/tseemann/abricate/blob/master/LICENSE"

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        bioperl \
        ncbi-blast+ \
        gzip \
        unzip \
        git \
        libjson-perl \
        libtext-csv-perl \
        libpath-tiny-perl \
        liblwp-protocol-https-perl \
        libwww-perl \
    && rm -rf /var/lib/apt/lists/*

# Downloading source code and help files
RUN git clone https://github.com/tseemann/any2fasta.git
RUN cp any2fasta/any2fasta /usr/local/bin

WORKDIR /opt
RUN git clone https://github.com/tseemann/abricate.git
RUN chmod -R a+x /opt/abricate
RUN /opt/abricate/bin/abricate --check
RUN /opt/abricate/bin/abricate --setupdb
RUN /opt/abricate/bin/abricate /opt/abricate/test/assembly.fa

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/abricate/bin/

# for singularity compatibility
ENV LC_ALL=C

# simple executor
CMD ["abricate"]

