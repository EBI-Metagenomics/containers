FROM mambaorg/micromamba:2.9.0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="gemsparcl"
LABEL software.version="078c47d"

COPY --chown=${MAMBA_USER}:${MAMBA_USER} env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml \
    && micromamba clean --all --yes \
    && rm /tmp/env.yaml

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # (otherwise python will not be found)

# Git source: https://github.com/johannahelene/gemsparcl (requested ref: main, resolved commit: 078c47d)
RUN python -m pip install --no-cache-dir git+https://github.com/johannahelene/gemsparcl@078c47dbbc1a45f7ab2532666da13f4f2aaab6b8

WORKDIR /data
CMD ["/bin/bash", "-c"]
