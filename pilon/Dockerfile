# Docker file for Pilon
FROM ubuntu:20.04

ENV pilonVer=1.24

LABEL software="pilon"
LABEL software.version="${pilonVer}"
LABEL description="Pilon is a software tool to automatically improve draft assemblies and to find variation among strains, including large event detection."
LABEL website="https://github.com/broadinstitute/pilon"
LABEL license="https://github.com/broadinstitute/pilon/blob/master/LICENSE"


# install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
        default-jre-headless \
        wget

# install pilon
WORKDIR /opt
RUN wget -q https://github.com/broadinstitute/pilon/releases/download/v${pilonVer}/pilon-${pilonVer}.jar && \
    mv pilon-${pilonVer}.jar pilon.jar

# for singularity compatibility
ENV LC_ALL=C

# setting workdir
RUN mkdir /data
WORKDIR /data

# simple executor
CMD ["/bin/bash", "-c"]