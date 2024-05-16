FROM python:3.9-slim

ENV VERSION="1.4.0"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL version="${VERSION}"
LABEL software="pyCirclize"
LABEL website="https://github.com/moshi4/pyCirclize"
LABEL license="https://github.com/moshi4/pyCirclize/blob/main/LICENSE"

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# install pyCirclize via pip
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
    matplotlib==3.9.0 \
    pycirclize==${VERSION}

