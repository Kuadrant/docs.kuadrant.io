FROM registry.access.redhat.com/ubi9/python-39

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /docs

COPY pyproject.toml .

RUN uv venv $HOME/venv && \
    . $HOME/venv/bin/activate && \
    uv pip install -r pyproject.toml

ENV PATH="$HOME/venv/bin:$PATH"

VOLUME /docs

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["mkdocs", "serve", "-s", "-a", "0.0.0.0:8000"]
