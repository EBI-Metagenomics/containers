FROM continuumio/miniconda3

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

LABEL base_image="continuumio/miniconda3"
LABEL version="1"
LABEL software="dbcan"
LABEL software.version="4.0.0"


# set work dir
WORKDIR /app

RUN conda install -c conda-forge -c bioconda python=3.8 diamond hmmer prodigal dbcan=4.0.0 && \
    conda clean -ya 
    

RUN echo "source activate run_dbcan" > ~/.bashrc
ENV PATH /opt/conda/envs/run_dbcan/bin:$PATH

CMD ["/bin/bash", "-c"]
