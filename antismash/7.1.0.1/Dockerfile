FROM continuumio/miniconda3:23.10.0-1

LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

LABEL base_image="continuumio/miniconda3"
LABEL version="1"
LABEL software="antismash"
LABEL software.version="7.1.0.1"

ENV VERSION=7-1-0-1

RUN conda install -c bioconda -c conda-forge\
    'python>=3.9' \
    'brawn>=1.0.1' \
    numpy \
    biopython=1.78 \
    'helperlibs>=0.2.1' \
    jinja2 \
    joblib \
    jsonschema \
    'markupsafe>=2.0' \
    pysvg-py3 \
    bcbio-gff \
    libsass \
    matplotlib-base \
    scipy \
    'scikit-learn>=1.3.2' \
    'moods>=1.9.4' \
    diamond \
    'fasttree=2.1.*' \
    'glimmerhmm=3.0.*' \
    hmmer2 \
    'hmmer>=3.1b2' \
    'meme==4.11.2' \
    blast \
    prodigal \
    nodejs \
    --yes --freeze-installed && conda clean -afy

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir 'nrpys>=0.1.1'

WORKDIR /opt

RUN wget https://github.com/antismash/antismash/archive/refs/tags/$VERSION.tar.gz -O antismash_$VERSION.tar.gz && \
    mkdir -p antismash && tar -xzvf antismash_$VERSION.tar.gz -C antismash --strip-components=1 && \
    rm antismash_$VERSION.tar.gz

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -U antismash/

# Download, configure the DBs and then delete them
RUN PYTHONDONTWRITEBYTECODE=1 python /opt/antismash/antismash/download_databases.py --database-dir /opt/antismash_databases && \
    rm -r /opt/antismash_databases

ENV PATH=/opt/conda/bin:${PATH}

