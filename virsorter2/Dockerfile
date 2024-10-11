# Use Ubuntu as the base image to have apt-get available
FROM ubuntu:20.04

# Install micromamba
RUN apt-get update && apt-get install -y curl bzip2 \
    && curl -L https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj -C /usr/local/bin --strip-components=1 bin/micromamba

# Set the root prefix for micromamba
ENV MAMBA_ROOT_PREFIX=/opt/micromamba

# Create the root prefix directory
RUN mkdir -p /opt/micromamba

# Set the working directory in the container
WORKDIR /app

# Install additional system utilities using apt-get
RUN apt-get update && apt-get install -y \
    original-awk \
    dateutils \
    procps \
    pcregrep \
    sed

# Install mamba and create the 'vs2' environment with virsorter>=2.2.4
# https://github.com/jiarong/VirSorter2/blob/9f8ae48279ebfb906558b233f6fc84fa5cc1d390/virsorter/envs/vs2.yaml
RUN micromamba create -n vs2 -c conda-forge -c bioconda \
                                               virsorter>=2.2.4-1 \
                                               "python>=3.6,<=3.10" \
                                               scikit-learn=0.22.1 \
                                               imbalanced-learn \
                                               seaborn \
                                               hmmer==3.3 \
                                               prodigal=2.6 \
                                               screed==1 \
                                               ruamel.yaml \
                                               "snakemake>=5.18,<=5.26" \
                                               click \
                                               "conda-package-handling<=1.9" \
                                               pandas==1.2 \
                                               numpy==1.23 \
    && micromamba clean --all --yes

# Activate the 'vs2' environment by default when the container starts
SHELL ["micromamba", "run", "-n", "vs2", "--"]

# Set up an entrypoint to ensure the environment is activated
ENTRYPOINT ["micromamba", "run", "-n", "vs2"]

ENV PATH=/opt/micromamba/envs/vs2/bin:$PATH
# By default, start an interactive shell
CMD ["bash"]
