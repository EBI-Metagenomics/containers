FROM quay.io/microbiome-informatics/miniconda:4.11.0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="quay.io/microbiome-informatics/miniconda:4.11.0"
LABEL software="emeraldBGC"
LABEL software.version="0.2.4.1"
LABEL about.license="SPDX:Apache-2.0"
LABEL about.home="https://github.com/Finn-Lab/emeraldBGC"

WORKDIR /opt/

RUN conda config --add channels bioconda && \
    conda config --add channels conda-forge

RUN mamba install -y \
    python=3.9 \
    perl>=5 \
    biopython=1.79 \
    numpy=1.16 \
    openjdk=11.0 \
    tensorflow=2.4 \
    hmmer=3.3.2 \
    joblib=1.0.1 \
    scikit-learn=0.24 \
    prodigal=2.6.3 \
    && conda clean -afy

RUN wget -q https://github.com/Finn-Lab/emeraldBGC/archive/refs/tags/v0.2.4.1.tar.gz && \
    tar -xzf v0.2.4.1.tar.gz && \
    pip install -U emeraldBGC-0.2.4.1/ && \
    rm v0.2.4.1.tar.gz && rm -r emeraldBGC-0.2.4.1/

ENV PATH /opt/miniconda/bin/:${PATH}

WORKDIR /data

CMD ["/bin/bash", "-c"]
