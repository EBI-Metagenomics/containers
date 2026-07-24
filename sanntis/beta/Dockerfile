FROM mambaorg/micromamba:2.5.0

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml

RUN micromamba install --yes --file /tmp/env.yaml && \
    micromamba clean --all --yes

    ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN mamba install -y \
    python=3.9 \
    perl>=5 \
    hmmer=3.3.2 \
    scikit-learn=0.24 \
    prodigal=2.6.3 \
    && conda clean -afy

RUN wget -q https://github.com/Finn-Lab/SanntiS/archive/refs/tags/v0.9.3.4.tar.gz && \
    tar -xzf v0.9.3.4.tar.gz && \
    pip install -U SanntiS-0.9.3.4/ && \
    rm v0.9.3.4.tar.gz && rm -r SanntiS-0.9.3.4/

ENV PATH /opt/miniconda/bin/:${PATH}

WORKDIR /data

CMD ["/bin/bash", "-c"]
