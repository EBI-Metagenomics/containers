FROM quay.io/biocontainers/gtdbtk:2.3.0--pyhdfd78af_0

LABEL software="GTDB-Tk"
LABEL software.version="2.3.0"
LABEL description="A toolkit for assigning objective taxonomic classifications to bacterial and archaeal genomes."
LABEL website="https://github.com/Ecogenomics/GTDBTk"
LABEL license="GPLv3"

ENV VERSION=2.3.0

WORKDIR /opt/gtdbtk_src

RUN wget https://github.com/Ecogenomics/GTDBTk/archive/refs/tags/${VERSION}.tar.gz -O gtdbtk_${VERSION}.tar.gz && \
    tar -xzvf gtdbtk_${VERSION}.tar.gz --strip-components=1 && \
    wget https://raw.githubusercontent.com/Ecogenomics/GTDBTk/0a7ff4a97aa1d538a878f3a339d8959e634c61ef/scripts/gtdb_to_ncbi_majority_vote.py -P /usr/local/bin && \
    chmod a+x /usr/local/bin/gtdb_to_ncbi_majority_vote.py

ENV PYTHONPATH="/opt/gtdbtk_src:${PYTHONPATH}"