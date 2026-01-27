FROM python:3.11-slim

LABEL description="Container with scikit-learn=1.5.2, pandas=2.2.2, xgboost=2.1.1 and PathOFact2 scripts"
LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

# Avoid interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# ---- PathoFact2 release parameters ----
ARG PATHOFACT2_TAG=submission-v1.0
ARG PATHOFACT2_PROJECT_URL=https://gitlab.com/uniluxembourg/lcsb/systems-ecology/pathofact2
# GitLab "Source code (tar.gz)" follows the archive pattern below
ARG PATHOFACT2_TARBALL_URL=${PATHOFACT2_PROJECT_URL}/-/archive/${PATHOFACT2_TAG}/pathofact2-${PATHOFACT2_TAG}.tar.gz

# Install system dependencies required for compiling Python packages and downloading files
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    procps \
    ca-certificates \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install python depedencies
RUN pip install --no-cache-dir \
    scikit-learn==1.5.2 \
    pandas==2.2.2 \
    xgboost==2.1.1


# Download + extract PathoFact2 source release, expose scripts
RUN mkdir -p /opt/pathofact2 \
    && curl -fsSL "${PATHOFACT2_TARBALL_URL}" -o /tmp/pathofact2.tar.gz \
    && tar -xzf /tmp/pathofact2.tar.gz -C /opt/pathofact2 \
    && rm -f /tmp/pathofact2.tar.gz

# Make the src scripts directly callable
ENV PATH="/opt/pathofact2/pathofact2-${PATHOFACT2_TAG}/src:${PATH}"

# Make scripts executable (if needed)
RUN chmod +x /opt/pathofact2/pathofact2-${PATHOFACT2_TAG}/src/*.py || true

WORKDIR /data

CMD ["/bin/bash", "-c"]
