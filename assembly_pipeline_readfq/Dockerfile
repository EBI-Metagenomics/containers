FROM alpine:3.16.0

#tag  microbiome-informatics/assembly-pipeline.readfq:latest
LABEL maintainer="Microbiome Informatics Team www.ebi.ac.uk/metagenomics"

RUN apk add zlib-dev --no-cache gcc musl-dev; \
    mkdir /tools

COPY kseq.h \
     kseq_fastq_base.c \
/tools/

RUN chmod a+x /tools/*

RUN gcc -o kseq_fastq_base /tools/kseq_fastq_base.c -lz

#CMD ["./kseq_fastq_base"]
