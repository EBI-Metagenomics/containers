FROM mambaorg/micromamba:2.0.5

USER root

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

LABEL version="1"
LABEL software="owltools"
LABEL software.version="2024-06-12"

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba clean -a -y

ENV PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"

RUN wget https://github.com/owlcollab/owltools/releases/download/2024-06-12/owltools

RUN chmod +x owltools

RUN mv owltools /bin