# Central repository for containers used in the Microbiome Informatics Team at EMBL - EBI

## Using the Taskfile

This repository uses [Task](https://taskfile.dev) to simplify building and managing container images.

### Prerequisites

- Docker with buildx support
- Taskfile.dev installed (see https://taskfile.dev/installation/)

### Available Commands

#### Building Images

To build a container image locally for a specific tool and version:

```bash
task build TOOL=mgnify-pipelines-toolkit VERSION=1.4.9
```

This command builds a multi-platform image (linux/amd64 and linux/arm64) from the Dockerfile located in `mgnify-pipelines-toolkit/1.4.9/`. The image is tagged as `quay.io/microbiome-informatics/mgnify-pipelines-toolkit:1.4.9`.

#### Building and Pushing Images

To build and push an image directly to the Quay.io registry:

```bash
task build-push TOOL=mgnify-pipelines-toolkit VERSION=1.4.9
```

This performs the same build process but additionally pushes the resulting image to the registry. You must be authenticated to the `quay.io/microbiome-informatics` organization.

#### Listing Available Tools

To see all available tools and versions in the repository:

```bash
task list
```

This scans the directory structure and displays all tools with their available versions.

### Repository Structure

Each tool is organized in the following structure:

```
tool-name/
└── version/
    └── Dockerfile
```

For example, `mgnify-pipelines-toolkit/1.4.9/Dockerfile` contains the build instructions for version 1.4.9 of the MGnify Pipelines Toolkit.

### Image Registry

All images are pushed to the Quay.io registry under the `microbiome-informatics` organization. Images are available at [quay.io/microbiome-informatics](https://quay.io/repository/microbiome-informatics)