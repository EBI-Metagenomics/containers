FROM mambaorg/micromamba:2.1.1

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml

RUN micromamba install -y -n base -f /tmp/env.yaml \
    && micromamba install -y -n base conda-forge::procps-ng \
    && micromamba env export --name base --explicit > env.lock \
    && echo ">> CONDA_LOCK_START" \
    && cat env.lock \
    && echo "<< CONDA_LOCK_END" \
    && micromamba clean -a -y

USER root

ENV PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"

# The path /opt/conda/lib/python3.10/site-packages/genomeuploader has to be manually added otherwise
# the genome_uploader executable doesn't find the ena module (which lives in that folder)
ENV PYTHONPATH="/opt/conda/lib/python3.10/site-packages/genomeuploader:$PYTHONPATH"