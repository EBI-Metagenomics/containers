FROM quay.io/microbiome-informatics/miniconda:4.11.0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="quay.io/microbiome-informatics/miniconda:4.11.0"
LABEL software="DRAM"
LABEL software.version="1.3"
LABEL about.license="SPDX:GPL-3.0-or-later"
LABEL about.home="https://github.com/WrightonLabCSU/DRAM"

WORKDIR /opt/

RUN wget https://github.com/WrightonLabCSU/DRAM/archive/refs/tags/v1.3.tar.gz && \
    tar -xf v1.3.tar.gz && \
    rm -r v1.3.tar.gz

RUN mamba env update -n base --file DRAM-1.3/environment.yaml && conda clean -afy

ENV PATH /opt/miniconda/bin/:${PATH}

# for singularity compatibility
ENV LC_ALL=C

WORKDIR /data

CMD ["/bin/bash", "-c"]
