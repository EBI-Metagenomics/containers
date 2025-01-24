FROM mambaorg/micromamba:2.0.5

ARG VERSION=5.72-103.0

LABEL software="InterProScan"
LABEL software.version="5.72-103.0"
LABEL description="InterProScan is a search engine for InterPro is a database which integrates together predictive information about proteins' function."
LABEL website="https://github.com/ebi-pf-team/interproscan"
LABEL license="Apache 2.0"

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba env export --name base --explicit > environment.lock \
    && cat environment.lock \
    && micromamba clean -a -y

ENV PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"

USER root

# Install InterProScan #
WORKDIR /opt

RUN wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/${VERSION}/alt/interproscan-core-${VERSION}.tar.gz && \
    tar -xzf interproscan-core-${VERSION}.tar.gz && \
    rm interproscan-core-${VERSION}.tar.gz

RUN cp /opt/interproscan-${VERSION}/interproscan.properties /opt/interproscan-${VERSION}/interproscan.properties.bak

COPY interproscan.properties /opt/interproscan-${VERSION}/interproscan.properties

ENV PATH="/opt/interproscan-${VERSION}/:$PATH"
