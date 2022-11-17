FROM ubuntu:20.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="0.0.1"
LABEL software="kegg-cwl"
LABEL website="https://github.com/EBI-Metagenomics/kegg-cwl"
LABEL license="https://github.com/EBI-Metagenomics/kegg-cwl/blob/master/LICENSE"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        wget \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*


# Dependencies
RUN pip3 install --upgrade pip && \
    pip3 install networkx

# Downloading KEGG help files to generate pathways
WORKDIR /
RUN mkdir /help_files
RUN wget ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/pipeline-5.0/ref-dbs/graphs.pkl.gz -P help_files && gzip -d /help_files/graphs.pkl.gz
RUN wget ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/pipeline-5.0/ref-dbs/all_pathways_names.txt.gz -P help_files && gzip -d /help_files/all_pathways_names.txt.gz
RUN wget ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/pipeline-5.0/ref-dbs/all_pathways_class.txt.gz -P help_files && gzip -d /help_files/all_pathways_class.txt.gz

# Add .py scripts
RUN mkdir /tools
ADD Tools/give_pathways.py /tools/give_pathways.py
ADD run_pathways.sh /tools/run_pathways.sh

RUN chmod -R a+rwx /tools
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/tools

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
