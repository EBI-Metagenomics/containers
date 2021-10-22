# Dockerfile for Prodigal
FROM alpine:3.14.1

ENV prodigalVer=2.6.3

LABEL software="prodigal"
LABEL software.version="${prodigalVer}"
LABEL description="Prodigal is gene prediction program"
LABEL website="https://github.com/hyattpd/Prodigal"
LABEL license="https://github.com/hyattpd/Prodigal/blob/GoogleImport/LICENSE"

# install deps
RUN apk add --no-cache bash

# install prodigal
WORKDIR /usr/local/bin
RUN wget -q -O prodigal https://github.com/hyattpd/Prodigal/releases/download/v${prodigalVer}/prodigal.linux
RUN chmod +x /usr/local/bin/prodigal

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]