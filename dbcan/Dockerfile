FROM quay.io/microbiome-informatics/miniconda:4.11.0

ENV VERSION="3.0.4"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="${VERSION}"
LABEL software="dbCAN"
LABEL website="https://github.com/linnabrown/run_dbcan"
LABEL license="https://github.com/linnabrown/run_dbcan/blob/master/LICENSE"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    rm -rf /var/lib/apt/lists/*


# install conda packages
RUN conda install -c anaconda conda-build \
  && conda install wget \
  && conda install -c bioconda -y diamond hmmer prodigal \
  && conda clean -a

# install dbcan via pip
RUN pip install dbcan==${VERSION}

# directory for db
RUN mkdir /db

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
