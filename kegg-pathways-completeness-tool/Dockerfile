FROM alpine:3.14

LABEL Maintainer="Ekaterina Sakharova <kates@ebi.ac.uk>"

# Install dependencies and Git
RUN apk add --no-cache --update-cache --update python3 gzip git && \
    apk add --no-cache --update py3-pip && \
    apk add --no-cache --update bash && \
    git clone https://github.com/EBI-Metagenomics/kegg-pathways-completeness-tool.git && \
    pip3 install --upgrade pip && \
    pip3 install -r kegg-pathways-completeness-tool/requirements.txt

# Add KEGG files to generate pathways
RUN mkdir /pathways_data && \
mv kegg-pathways-completeness-tool/pathways_data/* /pathways_data/ && \
mv kegg-pathways-completeness-tool/graphs/graphs.pkl /pathways_data/ && \
mkdir /tools && \
mv kegg-pathways-completeness-tool/bin/give_pathways.py /tools/ && \
mv kegg-pathways-completeness-tool/bin/plot_completeness_graphs.py /tools/ && \
mv kegg-pathways-completeness-tool/docker/run_pathways.sh /tools/

# Set permissions for scripts
RUN chmod a+x /tools/give_pathways.py /tools/run_pathways.sh /tools/plot_completeness_graphs.py

# Set environment variable for tools directory
ENV PATH="/tools:${PATH}"
