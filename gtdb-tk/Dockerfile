FROM ubuntu:21.04

LABEL software="GTDB-Tk"
LABEL software.version="1.7.0"
LABEL description="A toolkit for assigning objective taxonomic classifications to bacterial and archaeal genomes."
LABEL website="https://github.com/Ecogenomics/GTDBTk"
LABEL license="GPLv3"

# Dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        python3 \
        python3-pip

# Install GTDB-Tk with pip
RUN pip3 install gtdbtk

# Workdir
RUN mkdir /data
WORKDIR /data

# reference data mount point
RUN mkdir /refdata
ENV GTDBTK_DATA_PATH=/refdata

# Entrypoint
CMD ["/bin/bash", "-c"]
