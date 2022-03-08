FROM quay.io/microbiome-informatics/miniconda:4.11.0

ARG metawrapVer="1.3.2"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="${metawrapVer}"
LABEL software="metaWRAP"
LABEL website="https://github.com/bxlab/metaWRAP"
LABEL license="https://github.com/bxlab/metaWRAP/blob/master/LICENSE"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        git \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
RUN conda config --add channels defaults && \
    conda config --add channels conda-forge && \
    conda config --add channels bioconda

RUN mamba install -y \
        biopython=1.68 \
        blas=2.5=mkl \
        blast=2.6.0 \
        bmtagger=3.101 \
        bowtie2=2.3.5 \
        bwa=0.7.17 \
        checkm-genome=1.0.12 \
        concoct=1.0.0 \
        fastqc=0.11.8 \
        kraken=1.1 \
        kraken2=2.0 \
        krona=2.7 \
        matplotlib-base=2.2.3 \
        maxbin2=2.2.6 \
        megahit=1.1.3 \
        metabat2=2.12.1 \
        openssl=1.1 \
        pandas=0.24.2 \
        perl-bioperl \
        pplacer=1.1.alpha19 \
        prokka=1 \
        quast=5.0.2 \
        r-ggplot2=3.1.0 \
        r-reshape2 \
        r-recommended=3.5.1 \
        salmon=0.13.1 \
        samtools=1.9 \
        seaborn=0.9.0 \
        spades=3.13.0 \
        taxator-tk=1.3.3e \
        trim-galore=0.5.0 \
        python=2.7.15    ##for dep resolution

# Downloading source code
WORKDIR /opt
RUN git clone https://github.com/bxlab/metaWRAP.git

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/miniconda/bin/:/opt/metaWRAP/bin

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
#RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
