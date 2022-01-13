FROM ubuntu:20.04

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL base_image="ubuntu:20.04"
LABEL version="2.13"
LABEL software="mmseqs"
LABEL software.version="45111b6"
LABEL website="https://github.com/soedinglab/MMseqs2/releases"
LABEL license="https://github.com/soedinglab/MMseqs2/blob/master/LICENSE.md"

# install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        wget \
    && rm -rf /var/lib/apt/lists/*

# install mmseqs2
RUN mkdir /tools
WORKDIR /tools
ENV mmseqsVer=13-45111
RUN wget -q https://github.com/soedinglab/MMseqs2/releases/download/$mmseqsVer/mmseqs-linux-sse41.tar.gz && \
    tar zxf mmseqs-linux-sse41.tar.gz && \
    rm -rf mmseqs-linux-sse41.tar.gz mmseqs/userguide.pdf mmseqs/examples && \
    ln -s /tools/mmseqs/bin/mmseqs /usr/local/bin

# aux scripts
COPY mmseqs_wf_without_symlinks.sh /usr/local/bin/mmseqs_wf.sh
RUN chmod a+x /usr/local/bin/*

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
