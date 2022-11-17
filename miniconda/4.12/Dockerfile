FROM continuumio/miniconda3:4.12.0

LABEL software="miniconda"
LABEL software.version=4.12.0
LABEL description="Miniconda base image to install BioConda recipes, it contains the required tools for Nextflow metrics too."
LABEL website="https://docs.conda.io/en/latest/miniconda.html"
LABEL license="https://www.anaconda.com/end-user-license-agreement-miniconda"

RUN apt-get update -q && \
    apt-get install -q -y --no-install-recommends \
        original-awk \
        dateutils \
        procps \
        pcregrep \
        sed \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
