FROM quay.io/microbiome-informatics/miniconda:4.11.0

#tag microbiome-informatics/assembly-pipeline.python3_scripts:3.7.9
LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="assembly-pipeline.python"
LABEL software.version="1.0.0"
LABEL website="https://github.com/EBI-Metagenomics/CWL-assembly/tree/develop/cwl"
LABEL license="https://github.com/EBI-Metagenomics/CWL-assembly/blob/develop/LICENSE"

# Dependencies
RUN conda config --add channels bioconda && \
    conda config --add channels conda-forge

RUN mamba install -c conda-forge -y biopython && \
    conda clean -afy

COPY gen_stats_report.py \
     trim_fasta.py \
/data/

RUN chmod a+x /data/*

ENV PATH /opt/miniconda/bin/:/data/:${PATH}

# for singularity compatibility
ENV LC_ALL=C
