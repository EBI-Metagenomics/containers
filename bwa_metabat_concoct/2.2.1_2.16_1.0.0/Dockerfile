# Docker container for BWA, metabat2 and concoct

# Use a base image with Miniconda
FROM debian:buster AS apt-get-tools
# Install system dependencies
RUN apt-get update \
    && apt-get install -q -y --no-install-recommends \
            original-awk \
            dateutils \
            procps \
            pcregrep \
            sed \
    && rm -rf /var/lib/apt/lists/*

FROM continuumio/miniconda3:4.9.2 AS miniconda
COPY --from=apt-get-tools / /

# Install conda packages
RUN conda install -y -c bioconda -c conda-forge concoct=1.0.0 bwa-mem2=2.2.1 metabat2=2.15 \
    && conda clean --all