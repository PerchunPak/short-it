FROM python:3.11-slim AS poetry

ENV PATH "/root/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED 1

WORKDIR /root
# see DOK-DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install curl -y --no-install-recommends && \
    curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry export --no-interaction -o requirements.txt --without-hashes --only main,docker


FROM python:3.11-slim AS base

ENV PYTHONPATH "/app"

WORKDIR /app

RUN groupadd -g 5000 container && useradd -d /app -m -g container -u 5000 container
COPY --from=poetry /root/requirements.txt ./
RUN pip --no-cache-dir install -U pip && \
    pip --no-cache-dir install -r requirements.txt
COPY short_it/ short_it/


FROM python:3.11-slim AS git
# Write version for the Sentry 'release' option
# (`apt-get update` because without it `package not found`, even if this update already was in `base` step)
RUN apt-get update && \
    apt-get install git -y --no-install-recommends
COPY .git .git
RUN git rev-parse HEAD > /commit.txt


FROM base AS final

COPY --from=git /commit.txt commit.txt
RUN chown -R 5000:5000 /app
USER container

ENV SENTRY_ENVIRONMENT production

CMD ["dumb-init", "uvicorn", "short_it.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
