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
    cp /opt/gtdbtk_src/scripts/gtdb_to_ncbi_majority_vote.py /usr/local/bin

ENV PYTHONPATH="/opt/gtdbtk_src:${PYTHONPATH}"