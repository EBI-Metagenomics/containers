FROM ubuntu:latest

LABEL maintainer="Bertrand Neron"
LABEL maintainer.email="bneron@pasteur.fr"
LABEL authors="Jean Cury; Thomas Jove; Marie Touchon; Bertrand Neron; Eduardo PC Rocha"
LABEL package.version="2.0master"
LABEL package.license="GPLv3"
LABEL package.homepage="https://github.com/gem-pasteur/Integron_Finder/"
LABEL publications="https://doi.org/10.1093/nar/gkw319"

ARG DEBIAN_FRONTEND=noninteractive
ARG IF_GIT_URL="https://github.com/gem-pasteur/Integron_Finder.git"
ARG IF_GIT_TAG="fix_find_attc_max"
ARG COMMIT_ID="71ee6e0"

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y python3 python3-pip python3-venv git hmmer infernal prodigal vim

RUN cd /usr/local/src &&\
    git clone ${IF_GIT_URL} integron_finder && \
    cd integron_finder && \
    git checkout ${COMMIT_ID} . && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install .

ENV PATH=/usr/local/src/integron_finder/venv/bin:$PATH

CMD ["/bin/bash", "-c"]