FROM maven:3.9.9-eclipse-temurin-23-noble

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

LABEL version="1"
LABEL software="owltools"
LABEL software.version="2024-06-12"

RUN apt install git

RUN git clone https://github.com/owlcollab/owltools.git && \
    cd /owltools/OWLTools-Parent && \
    mvn clean install

ENV PATH="$PATH:/owltools/OWLTools-Runner/target"
