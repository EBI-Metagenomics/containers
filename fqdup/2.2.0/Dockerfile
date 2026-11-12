FROM debian:bookworm-slim

LABEL software="fqdup"
LABEL software.version="2.2.0"
LABEL description="FASTQ deduplication for ancient DNA libraries, with damage-aware hashing and PCR error correction."
LABEL website="https://github.com/genomewalker/fqdup"

# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        ca-certificates \
        procps \
        zlib1g-dev \
        libzstd-dev \
        libxxhash-dev \
        libhts-dev \
        libisal-dev \
        libjemalloc-dev \
    && rm -rf /var/lib/apt/lists/*

# libtaph must be a clean checkout of the SHA in fqdup's LIBTAPH_PIN (enforced by CMake);
# flat_hash_map and BBHash float on master upstream, so pin them here
WORKDIR /opt
RUN git clone https://github.com/genomewalker/fqdup.git && git -C fqdup checkout v2.2.0 && \
    git clone https://github.com/genomewalker/libtaph.git && git -C libtaph checkout "$(cat fqdup/LIBTAPH_PIN)" && \
    git clone https://github.com/skarupke/flat_hash_map.git && git -C flat_hash_map checkout 2c4687431f978f02a3780e24b8b701d22aa32d9c && \
    git clone https://github.com/rizkg/BBHash.git && git -C BBHash checkout be4220c8f8580299b212a0c6c6c867528a0f07ac

# x86-64-v3 is the upstream default (AVX2), arm64 uses the scalar code paths
RUN if [ "$(uname -m)" = "aarch64" ]; then MARCH=armv8-a; else MARCH=x86-64-v3; fi && \
    cmake -S fqdup -B fqdup/build \
        -DCMAKE_BUILD_TYPE=Release \
        -DFQDUP_MARCH=${MARCH} \
        -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
        -DFETCHCONTENT_SOURCE_DIR_LIBTAPH=/opt/libtaph \
        -DFETCHCONTENT_SOURCE_DIR_FLAT_HASH_MAP=/opt/flat_hash_map \
        -DFETCHCONTENT_SOURCE_DIR_BBHASH=/opt/BBHash && \
    cmake --build fqdup/build --target fqdup --parallel $(nproc) && \
    bash fqdup/tests/smoke.sh /opt/fqdup/build/fqdup && \
    mv fqdup/build/fqdup /usr/local/bin/ && \
    rm -rf /opt/fqdup /opt/libtaph /opt/flat_hash_map /opt/BBHash

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]
