FROM ubuntu:20.04

ENV VERSION="2.12.0"

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="Blast"
LABEL version="${VERSION}"
LABEL description="Basic local alignment search tool"
LABEL webpage="https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastHome"
LABEL license="https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/lxr/source/scripts/projects/blast/LICENSE"

WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt install -y wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/${VERSION}/ncbi-blast-${VERSION}+-x64-linux.tar.gz && \
    tar -xzf ncbi-blast-${VERSION}+-x64-linux.tar.gz && \
    rm ncbi-blast-${VERSION}+-x64-linux.tar.gz

ENV PATH /app/ncbi-blast-${VERSION}+/bin:$PATH

CMD ["/bin/bash", "-c"]