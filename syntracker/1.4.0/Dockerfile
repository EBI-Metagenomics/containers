# SynTracker: strain tracking via genome synteny
# https://github.com/leylabmpi/SynTracker
#
# Built multi-arch (linux/amd64 + linux/arm64) via the repo Taskfile:
#   task build-push TOOL=syntracker VERSION=1.4.0
#
# Why not a plain `conda env create` from SynTracker_env.yml?
#   - bioconductor-decipher has NO linux-aarch64 build on bioconda, so a pure
#     conda install cannot resolve on the arm64 leg of the multi-arch build.
#   - The upstream pins (r-base=4.0.5, r-tidyverse=1.3.0) also no longer co-solve
#     against current DECIPHER (which needs r-base >=4.3).
# Fix: install what IS multi-arch on conda (python, r-base, r-tidyverse, blast),
# then install DECIPHER from Bioconductor source, which builds on any arch.
#
# miniforge3 is a multi-arch base (amd64 + arm64) with conda-forge as default.
FROM condaforge/miniforge3:24.9.2-0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="condaforge/miniforge3:24.9.2-0"
LABEL software="SynTracker"
LABEL software.version="1.4.0"
LABEL description="A pipeline for tracking closely related microbial strains using genome synteny."
LABEL website="https://github.com/leylabmpi/SynTracker"
LABEL license="SPDX:BSD-3-Clause"

# Build toolchain: needed to compile DECIPHER and its Bioconductor deps from source.
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Provided automatically by buildx per build leg (amd64 / arm64).
ARG TARGETARCH
ARG SYNTRACKER_VERSION=1.4.0
WORKDIR /opt
RUN git clone --depth 1 --branch "${SYNTRACKER_VERSION}" \
        https://github.com/leylabmpi/SynTracker.git syntracker || \
    git clone --depth 1 --branch "v${SYNTRACKER_VERSION}" \
        https://github.com/leylabmpi/SynTracker.git syntracker || \
    git clone --depth 1 https://github.com/leylabmpi/SynTracker.git syntracker

# Conda deps. Same set as SynTracker_env.yml plus BLAST+ (external requirement)
# and BiocManager. Pins dropped deliberately so the solver picks a mutually
# compatible modern set.
#
# DECIPHER is handled per-architecture, and mamba is invoked EXACTLY ONCE per
# leg (mutating the base env and then re-invoking mamba breaks its own libs
# under QEMU emulation -> "libxml2.so.2: cannot open shared object file"):
#   amd64 -> add the prebuilt bioconda DECIPHER binary to this single solve
#            (source-compiling it under the amd64 emulator fails with
#            "Exec format error").
#   arm64 -> bioconda has no linux-aarch64 DECIPHER build, so it is compiled
#            from Bioconductor source in the next step, which runs natively.
RUN if [ "$TARGETARCH" = "arm64" ]; then DECIPHER_PKG=""; else DECIPHER_PKG="bioconductor-decipher"; fi && \
    mamba install -y -n base -c conda-forge -c bioconda \
        python \
        r-base \
        r-tidyverse \
        r-biocmanager \
        blast \
        $DECIPHER_PKG && \
    conda clean -afy

# arm64 only: build DECIPHER from source (no mamba call here). Native, no emulation.
RUN if [ "$TARGETARCH" = "arm64" ]; then \
        Rscript -e 'BiocManager::install("DECIPHER", update=FALSE, ask=FALSE)'; \
    fi && \
    Rscript -e 'library(DECIPHER); cat("DECIPHER", as.character(packageVersion("DECIPHER")), "\n")'

ENV PATH=/opt/conda/bin:${PATH}
# for singularity compatibility
ENV LC_ALL=C

# Build-time sanity check of the full toolchain.
RUN python --version && blastn -version && \
    Rscript -e 'suppressMessages({library(DECIPHER); library(tidyverse)}); cat("R deps OK\n")'

WORKDIR /data
CMD ["python", "/opt/syntracker/syntracker.py", "--help"]
