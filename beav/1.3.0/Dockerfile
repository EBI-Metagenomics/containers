FROM quay.io/biocontainers/beav:1.3.0--hdfd78af_0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="quay.io/biocontainers/beav:1.3.0--hdfd78af_0"
LABEL software="beav"
LABEL software.version="1.3.0"
LABEL about.license="SPDX:GPL-3.0"
LABEL about.home="https://github.com/weisberglab/beav"

RUN . /usr/local/env-activate.sh && beav_db

WORKDIR /data

CMD ["/bin/bash", "-c"]