# Dockerfile for minimap2

FROM microbiomeinformatics/minimap2:2.22

LABEL software="Minimap2_filter"
LABEL software.version="2.22"
LABEL description="Minimap2 is a versatile sequence alignment program that aligns DNA or mRNA sequences against a large reference database. This tool filter host sequences"
LABEL website="https://github.com/lh3/minimap2"
LABEL license="https://github.com/lh3/minimap2/blob/master/LICENSE.txt"

# install deps
RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        samtools \
    && rm -rf /var/lib/apt/lists/*


# aux scripts
COPY minimap2_filter.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/minimap2_filter.sh

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]