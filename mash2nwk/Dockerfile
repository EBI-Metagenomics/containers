FROM rocker/r-ver:4.1.0

LABEL software="mash2nwk"
LABEL software.version="1.0.0"
LABEL description="Generate Mash distance tree of conspecific genomes"
LABEL website="https://github.com/EBI-Metagenomics/genomes-pipeline"
LABEL license="GPLv3"

RUN apt-get update \
    && apt-get install -q -y --no-install-recommends \
            procps \
            original-awk \
            dateutils \
            procps \
            pcregrep \
            sed \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && R -e "install.packages(c('reshape2', 'fastcluster', 'optparse', 'data.table', 'ape'), repos='http://cran.rstudio.com/')" \
    && rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN mkdir /tools
COPY mash2nwk1.R /tools
RUN chmod a+x /tools/*
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/tools

# Workdir
RUN mkdir /data
WORKDIR /data

# Entrypoint
CMD ["Rscript", "/tools/mash2nwk1.R"]