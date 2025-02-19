FROM mambaorg/micromamba:2.0.5

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba env export --name base --explicit > environment.lock \
    && cat environment.lock \
    && micromamba clean -a -y

# Add version information
ADD https://api.github.com/repos/EBI-Metagenomics/EukCC/git/refs/tags/v.2.1.3 version.json

ENV PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"