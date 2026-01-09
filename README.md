# Kuadrant Docs

## Overview

This repository contains documentation for Kuadrant, built using MkDocs and the `mike` plugin for multi-versioning. You can run and build these docs using Docker/Podman or by installing MkDocs locally.

## Contributing

See [./CONTRIBUTING.md](./CONTRIBUTING.md)

## Using Docker/Podman

### Running the Docs with Docker

To run the docs using Docker, mount the current directory to the container and bind it to port `8000`:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  -p 8000:8000 quay.io/kuadrant/docs.kuadrant.io:latest \
  "mkdocs serve -s -a 0.0.0.0:8000"
```

This will serve the docs at [http://localhost:8000](http://localhost:8000).

---

## Running Locally without Docker

### Installing uv

First, install `uv` (a fast Python package installer):

```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installing Dependencies

Install the project dependencies using `uv`:

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

You'll also need `asciidoctor` for AsciiDoc support:

```bash
# macOS
brew install asciidoctor

# Linux
gem install asciidoctor
```

### Serving the Docs Locally

To serve the docs locally, run:

```bash
mkdocs serve -s
```

You can then view the docs at [http://127.0.0.1:8000](http://127.0.0.1:8000) on your current branch.

### AsciiDoc Support

Both Markdown (`.md`) and AsciiDoc (`.adoc`) files are supported. AsciiDoc files are converted using [Asciidoctor](https://asciidoctor.org/) via the [mkdocs-asciidoctor-backend](https://github.com/aireilly/mkdocs-asciidoctor-backend) plugin.

To add an AsciiDoc page:

1. Create a `.adoc` file in `docs/`
2. Add it to the `nav` section in `mkdocs.yml`

Example AsciiDoc file:

```asciidoc
= Page Title

== Section

Some content with *bold* and _italic_ text.

[source,yaml]
----
apiVersion: v1
kind: ConfigMap
----
```

See `docs/install-helm.adoc` for an example.

### Running Multi-Versioned Docs

If you’d like to test the multi-versioned documentation setup locally, use `mike`:

```bash
mike serve
```

Or, with Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  -p 8000:8000 quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike serve -a 0.0.0.0:8000"
```

This will serve the docs from the `gh-pages` branch with multi-versioning. For general development, use `mkdocs serve`.

---

## Building the Docs

For automated builds, see the GitHub Actions workflows in `.github/workflows/build.yaml` and `.github/workflows/manual-deploy.yaml`.

---

## Using `mike` for Versioned Docs

We use `mike` for managing multi-versioned docs. It works by adding new commits to the `gh-pages` branch each time you run `mike deploy`. Older versions remain available without modification. If needed, existing versions can be re-built.

### Common `mike` Commands

#### List releases

Locally:

```bash
mike list
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike list"
```

#### Deploy a new release with a custom title

Locally:

```bash
mike deploy 1.0.x -t "1.0.x (latest stable)"
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike deploy 1.0.x -t '1.0.x (latest stable)'"
```

#### Delete a release

Locally:

```bash
mike delete 1.0.x
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike delete 1.0.x"
```

#### Serve multi-versioned docs

Locally:

```bash
mike serve -S
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  -p 8000:8000 quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike serve -a 0.0.0.0:8000"
```

---

## Mike Aliases

We use two aliases with `mike`:

- `latest`: Points to the latest stable release (e.g., `latest -> 1.0.x`)
- `dev`: Points to `HEAD` of `main`, for unstable or pre-release documentation

---

## Releases

Development releases from `main` will deploy to `dev` as a fast channel. The `latest` alias points to the most recent stable release by default.

Stable releases should be tagged (e.g., `git tag 0.6.1`) for clarity.

### Creating a Stable Release

To mark a new release as stable, follow these steps:

> **Note:** This process is currently manual and will be automated soon.

1. Create a release branch from `main` (e.g., `git checkout -b v1.0.x`).
2. In the release branch (`v1.0.x`):
    - Update `mkdocs.yml` to replace `branch=` references with specific tags for all components.
    - Set the latest release as default in `mkdocs.yml`:
      ```yaml
      extra:
        version:
          provider: mike
          default:
            - 1.0.x
            - latest
      ```
    - Update any other references for the new release, including `import_url` git refs and other version-specific settings.
3. Deploy the release with the `latest` alias:

Locally:

```bash
mike deploy --update-aliases 1.0.x latest --push
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike deploy --update-aliases 1.0.x latest --push --allow-empty"
```

4. Set this release as the default version:

Locally:

```bash
mike set-default 1.0.x --push
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike set-default 1.0.x --push --allow-empty"
```

5. Tag the repo (e.g., `git tag 1.0.x && git push --tags <upstream-origin>`).

---

## Re-Releasing Docs

Re-releasing an existing version is generally not recommended but can be done if necessary.

### Via GitHub Actions (Recommended)

To re-release a version, go to `Actions > Re-deploy via mike` in GitHub and run the workflow with the desired version and source branch.

For reference:

| Workflow Source | Version to Deploy | Source Branch | Notes               |
|-----------------|-------------------|---------------|---------------------|
| main            | 0.10.0            | 0.10.0        | Latest Stable       |
| main            | 0.8.0             | 0.8           |                     |
| main            | dev               | main          | Development - Unstable |

### Manual Re-release

1. Fetch latest changes: `git fetch --all`
2. Check out the release branch: `git checkout 0.7.x`
3. Make necessary changes and re-deploy:

Locally:

```bash
mike deploy 1.0.x -t "1.0.x" --push
```

Docker / Podman:

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  quay.io/kuadrant/docs.kuadrant.io:latest \
  "mike deploy 1.0.x -t '1.0.x' --push"
```

4. If there’s a push error, reset to the latest `gh-pages` branch and try again.

---

## Deploying

This site deploys automatically via GitHub Pages on merge to `main`. To manually trigger a deployment, go to `Actions > ci > Run Workflow`:

![Deploy](docs/assets/images/deploy.png)

This workflow will build the documentation bundle and trigger a push to the `gh-pages` branch.


## Building the Docker Image

### Single Architecture

```bash
docker build -t quay.io/kuadrant/docs.kuadrant.io:latest .
docker push quay.io/kuadrant/docs.kuadrant.io:latest
```

### Multi-Architecture (amd64 + arm64)

```bash
# create and use buildx builder
docker buildx create --name multiarch --use

# build and push for both architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t quay.io/kuadrant/docs.kuadrant.io:latest \
  --push .
```

**Note:** requires Docker Buildx and authentication to quay.io (`docker login quay.io`)


### Troubleshooting

#### Errors with the docs.kuadrant.io container

```bash
error: failed to push branch gh-pages to origin:
  /opt/app-root/src/.ssh/config: line 8: Bad configuration option: usekeychain
  /opt/app-root/src/.ssh/config: terminating, 1 bad configuration options
  fatal: Could not read from remote repository.

  Please make sure you have the correct access rights
  and the repository exists.
```

Remove the `usekeychain` option from your `~/.ssh/config` and try again.
