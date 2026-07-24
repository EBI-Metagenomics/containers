# Dockerfile for sourmash

# Dockerfile for sourmash
FROM continuumio/miniconda3:4.10.3p0

ENV sourmashVer=4.3.0

LABEL software="sourmash"
LABEL software.version="$sourmashVer"
LABEL description="Python library for computing hash sketches from DNA sequences, comparing them to each other, and plotting the results."
LABEL website="https://github.com/sourmash-bio/sourmash"
LABEL license="https://github.com/sourmash-bio/sourmash/blob/latest/LICENSE"

ENV DEBIAN_FRONTEND noninteractive
# install sourmash from BioConda
RUN conda update -n base -c defaults conda && \
    conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install sourmash==${sourmashVer} python=3.7 && \
    conda clean -a

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash" "-c"]