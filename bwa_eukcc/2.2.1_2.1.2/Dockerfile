FROM continuumio/miniconda3:4.9.2 AS miniconda

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

# BWA
FROM ubuntu:20.04 AS tools

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        build-essential \
        samtools \
        wget \
        bzip2 \
        cmake \
        git \
        libboost-all-dev \
        original-awk \
        dateutils \
        procps \
        pcregrep \
        sed \
    && rm -rf /var/lib/apt/lists/*

# install bwamem2
WORKDIR /tmp
ENV bwamem2Ver=2.2.1
RUN wget -q https://github.com/bwa-mem2/bwa-mem2/releases/download/v${bwamem2Ver}/bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    tar jxf bwa-mem2-${bwamem2Ver}_x64-linux.tar.bz2 && \
    mv bwa-mem2-${bwamem2Ver}_x64-linux/bwa-mem2* /usr/local/bin/ && \
    rm -rf bwa-mem2-${bwamem2Ver}_x64-linux*

COPY --from=miniconda /opt/conda/bin/ /opt/conda/bin/
COPY --from=miniconda /opt/conda/lib/ /opt/conda/lib/

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

ENV PATH="/opt/conda/bin:${PATH}"
#ENV PYTHONPATH="/opt/conda/lib/python3.8/site-packages:${PYTHONPATH}"

COPY ggp_binlinks.py /usr/local/bin/
RUN chmod +x /usr/local/bin/ggp_binlinks.py

# simple executor
CMD ["/bin/bash", "-c"]
