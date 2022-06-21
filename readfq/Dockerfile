FROM alpine:3.16.0

#tag  microbiome-informatics/readfq:latest
LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"
LABEL software="readfq"
LABEL software.version="1.0"
LABEL website="https://github.com/billzt/readfq"
LABEL license="https://github.com/lh3/readfq/blob/master/README"


RUN apk add zlib-dev --no-cache gcc musl-dev curl;

RUN mkdir /tools && \
    curl https://raw.githubusercontent.com/lh3/readfq/5fddb43d3220226f259aca023135ec0e25834bcf/kseq.h -o /tools/kseq.h

COPY kseq_fastq_base.c \
/tools/

RUN chmod a+x /tools/*

RUN gcc -o kseq_fastq_base /tools/kseq_fastq_base.c -lz