# SynTracker: strain tracking via genome synteny
# https://github.com/leylabmpi/SynTracker
#
# Build (amd64 ONLY):
#   docker buildx build --platform linux/amd64 -t quay.io/microbiome-informatics/syntracker:1.4.0 .
#
# Why amd64 only, with the upstream R pins:
#   SynTracker 1.4.0 targets SynTracker_env.yml: r-base=4.0.5, r-tidyverse=1.3.0 and the DECIPHER of
#   that era. A modern DECIPHER (>= 3.x, R >= 4.3) is NOT a drop-in: SynTracker.R calls
#   Seqs2DB(seqs, "XStringSet", <file path>, ...) outside its try() guard, and with a current
#   DECIPHER every per-region call errors ("N function calls resulted in an error"). SynTracker
#   then crashes in left_join() because no synteny table was produced.
#   The R 4.0-matched stack (DECIPHER 2.18.1 = Bioconductor 3.12) solves on linux-64 but has no
#   linux-aarch64 builds, so this image is amd64-only. Our HPC runners are x86_64 anyway, as is
#   the PopPUNK biocontainer.
FROM --platform=linux/amd64 condaforge/miniforge3:24.9.2-0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="condaforge/miniforge3:24.9.2-0"
LABEL software="SynTracker"
LABEL software.version="1.4.0"
LABEL description="A pipeline for tracking closely related microbial strains using genome synteny."
LABEL website="https://github.com/leylabmpi/SynTracker"
LABEL license="SPDX:BSD-3-Clause"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Pinned to the release tag. No fallback to the default branch: a silent fallback would ship
# different code under the same version label.
ARG SYNTRACKER_VERSION=1.4.0
RUN git clone --depth 1 --branch "${SYNTRACKER_VERSION}" \
        https://github.com/leylabmpi/SynTracker.git /opt/syntracker && \
    rm -rf /opt/syntracker/.git /opt/syntracker/Sample_Data /opt/syntracker/SynTracker_Manual.*

# Upstream SynTracker_env.yml pins, with DECIPHER pinned to the R 4.0 build and the rest of the
# R stack locked to what that solve picks. RSQLite is explicit because Seqs2DB writes an SQLite
# file. BLAST+ is SynTracker's external requirement (makeblastdb / blastn / blastdbcmd).
# A dedicated env (not base): base holds conda/mamba themselves, which must keep their own Python.
# One solve, strict channel priority, so nothing drifts to a newer R.
RUN conda config --set channel_priority strict && \
    mamba create -y -n syntracker --override-channels -c conda-forge -c bioconda \
        "python=3.9" \
        "r-base=4.0.5" \
        "r-tidyverse=1.3.0" \
        "r-dplyr=1.0.10" \
        "r-stringr=1.4.1" \
        "r-purrr=0.3.4" \
        "r-rsqlite=2.2.8" \
        "bioconductor-biostrings=2.58.0" \
        "bioconductor-decipher=2.18.1" \
        "blast=2.16.0" && \
    conda clean -afy

ENV PATH=/opt/conda/envs/syntracker/bin:/opt/conda/bin:${PATH}
# for singularity compatibility; TZ silences R's "Failed to locate timezone database"
ENV LC_ALL=C
ENV TZ=UTC

# `syntracker.py` on PATH, as the pipeline module calls it.
RUN printf '#!/bin/sh\nexec /opt/conda/envs/syntracker/bin/python /opt/syntracker/syntracker.py "$@"\n' \
        > /usr/local/bin/syntracker.py && \
    chmod +x /usr/local/bin/syntracker.py

# Build-time checks: toolchain versions, then the exact DECIPHER path that failed before:
# Seqs2DB into an on-disk SQLite db, then FindSynteny, on two tiny synthetic sequences.
RUN python --version && blastn -version && \
    Rscript -e 'suppressMessages({library(DECIPHER); library(tidyverse)}); \
        cat("R ", R.version$major, ".", R.version$minor, " DECIPHER ", as.character(packageVersion("DECIPHER")), \
            " dplyr ", as.character(packageVersion("dplyr")), "\n", sep=""); \
        set.seed(1); b <- paste(sample(c("A","C","G","T"), 3000, TRUE), collapse=""); \
        s <- DNAStringSet(c(Sample.1_c1 = b, Sample.2_c1 = b)); db <- tempfile(); \
        for (i in seq_along(s)) Seqs2DB(s[i], "XStringSet", db, sub("_.*", "", names(s)[i]), verbose=FALSE); \
        syn <- FindSynteny(db, maxSep=15, maxGap=15, verbose=FALSE); \
        stopifnot(nrow(syn[2,1][[1]]) > 0); unlink(db); cat("Seqs2DB + FindSynteny OK\n")' && \
    syntracker.py --help > /dev/null && echo "syntracker.py OK"

WORKDIR /data
CMD ["syntracker.py", "--help"]
