FROM registry.access.redhat.com/ubi9/python-39

WORKDIR /docs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /docs

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["mkdocs", "serve", "-s", "-a", "0.0.0.0:8000"]
