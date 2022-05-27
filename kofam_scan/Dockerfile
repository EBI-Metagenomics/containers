FROM quay.io/microbiome-informatics/miniconda:4.11.0

ENV VERSION="1.3.0"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="${VERSION}"
LABEL software="kofam_scan"
LABEL website="https://github.com/takaram/kofam_scan"
LABEL license="https://github.com/takaram/kofam_scan/blob/master/LICENSE.txt"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install parallel
    rm -rf /var/lib/apt/lists/*

# install conda packages
RUN conda install -c anaconda conda-build \
  && conda install -c conda-forge ruby \
  && conda install -c bioconda hmmer \
  && conda clean -a

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
