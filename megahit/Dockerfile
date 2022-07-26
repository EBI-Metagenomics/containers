# Docker container for MEGAHIT
FROM ubuntu:20.04

ARG megahitVer=1.2.9

LABEL software="MEGAHIT"
LABEL software.version="${megahitVer}"
LABEL description="MEGAHIT is an ultra-fast and memory-efficient NGS assembler. It is optimized for metagenomes, but also works well on generic single genome assembly (small or mammalian size) and single-cell assembly."
LABEL website="https://github.com/voutcn/megahit"
LABEL license="GPLv3.0"

RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        bzip2 \
        cmake \
        gzip \
        g++ \
        libgomp1 \
        make \
        python \
        zlib1g-dev \
        wget

RUN wget https://github.com/voutcn/megahit/archive/refs/tags/v1.2.9.tar.gz  && \
    tar zxf v${megahitVer}.tar.gz && \
    rm v${megahitVer}.tar.gz && \
    cd megahit-${megahitVer}

COPY megahit-${megahitVer} /opt/megahit
WORKDIR /opt/megahit

# install dependencies
RUN rm -rf build && \
    mkdir -p build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j4 install && \
    apt-get autoremove --purge -y \
        cmake \
        g++ \
        make \
        zlib1g-dev && \
    apt-get autoclean

# make install if needed

RUN megahit --test && megahit --test --kmin-1pass
ENTRYPOINT ["megahit"]