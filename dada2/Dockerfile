FROM continuumio/miniconda3:24.3.0-0

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

LABEL base_image="continuumio/miniconda3"
LABEL version="1"
LABEL software="dada2"
LABEL software.version="1.32"

RUN conda install -c conda-forge r-base=4.3.3 r-tidyverse=2.0.0 \
    r-data.table=1.15.2 --yes

RUN R -e "install.packages('BiocManager',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('box', dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "BiocManager::install(version = '3.18')"
RUN R -e "BiocManager::install('dada2', version = '3.18')"
RUN R -e "BiocManager::install('shortread', version = '3.18')"
