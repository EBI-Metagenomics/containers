# Use a base image with Debian for system dependencies
FROM debian:buster AS apt-get-tools

# Install system dependencies
RUN apt-get update \
    && apt-get install -q -y --no-install-recommends \
            original-awk \
            dateutils \
            procps \
            pcregrep \
            sed \
            make \
            gcc \
            g++ \
            zlib1g-dev \
            libbz2-dev \
            liblzma-dev \
            libcurl4-openssl-dev \
            default-libmysqlclient-dev \
            build-essential \
            pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Use Miniconda as the base image
FROM continuumio/miniconda3:4.9.2 AS miniconda

# Copy system dependencies from the first stage
COPY --from=apt-get-tools / /

# Set conda configurations and install conda packages
RUN conda config --set ssl_verify no \
    && conda install -y -c bioconda -c conda-forge \
            'metaeuk=4.a0f584d' pplacer \
            'epa-ng=0.3.8' python=3.8 hmmer=3.3 git \
            minimap2 bwa pysam biopython \
            samtools=1.12 \
            six \
    && conda clean --all \
    && pip install jsonpickle>=4.0.0 numpy>=1.24.4 ete3>=3.1.3

# Install EukCC
RUN pip install --no-deps eukcc
RUN pip install --no-cache-dir --force-reinstall mysqlclient

# Add version information
ADD https://api.github.com/repos/EBI-Metagenomics/EukCC/git/refs/tags/v.2.1.3 version.json

# Set the entry point for the container
ENTRYPOINT ["eukcc"]
