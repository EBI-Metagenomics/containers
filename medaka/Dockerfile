# Dokerfile for Medaka

FROM continuumio/miniconda3:4.10.3p0

LABEL software="Medaka"
LABEL software.version="1.4.4"
LABEL description="Medaka is a tool to create consensus sequences and variant calls from nanopore sequencing data."
LABEL website="https://github.com/nanoporetech/medaka"
LABEL license="https://github.com/nanoporetech/medaka/blob/master/LICENSE.md"

ENV DEBIAN_FRONTEND noninteractive
# install medaka from BioConda
RUN conda update -n base -c defaults conda && \
    conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install medaka==1.4.4 python==3.8 && \
    conda clean -a

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash" "-c"]