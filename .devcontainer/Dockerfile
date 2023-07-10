FROM mcr.microsoft.com/devcontainers/python:3.11

USER vscode
ENV PATH "/home/vscode/.local/bin:${PATH}"
WORKDIR /workspaces/short-it

COPY poetry.lock pyproject.toml ./

RUN sudo chown -R 1000:1000 /workspaces/short-it && \
    export DEBIAN_FRONTEND=noninteractive && \
    sudo apt-get update && \
    sudo apt-get upgrade -y && \
    sudo apt-get -y install --no-install-recommends curl make

RUN export PYTHONUNBUFFERED=1 && \
    curl -sSL https://install.python-poetry.org | python - && \
    poetry install
