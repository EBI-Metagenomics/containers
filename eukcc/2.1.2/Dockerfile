# Use a base image with Miniconda
FROM debian:buster AS apt-get-tools
# Install system dependencies
RUN apt-get update \
    && apt-get install -q -y --no-install-recommends \
            original-awk \
            dateutils \
            procps \
            pcregrep \
            sed \
    && rm -rf /var/lib/apt/lists/*

FROM continuumio/miniconda3:4.9.2 AS miniconda
COPY --from=apt-get-tools / /

# Set conda configurations and install conda packages
RUN conda config --set ssl_verify no \
    && conda install -y -c bioconda -c conda-forge \
            'metaeuk=4.a0f584d' pplacer \
            'epa-ng=0.3.8' python=3.8 hmmer=3.3 git \
            minimap2 bwa pysam biopython \
            samtools=1.12 \
    && conda clean --all \
    && pip install jsonpickle numpy ete3 \
    && pip install https://github.com/EBI-Metagenomics/EukCC/archive/refs/tags/v.2.1.2.zip

# Add version information
ADD https://api.github.com/repos/EBI-Metagenomics/EukCC/git/refs/tags/v.2.1.2 version.json

# Set the entry point for the container
ENTRYPOINT ["eukcc"]
