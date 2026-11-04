FROM mambaorg/micromamba:2.9.0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="mgnify-pipelines-toolkit"
LABEL software.version="1.5.6"

COPY --chown=${MAMBA_USER}:${MAMBA_USER} env.yaml /tmp/env.yaml

RUN micromamba install -y -n base -f /tmp/env.yaml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba clean --all --yes \
    && rm /tmp/env.yaml

ENV PATH="${MAMBA_ROOT_PREFIX}/bin:${PATH}"
