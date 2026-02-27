# Kuadrant Docs

## Overview

This repository builds the documentation site for Kuadrant using MkDocs, Material theme, and the `mkdocs-multirepo-plugin`. Content is pulled from multiple Kuadrant repositories and published as a single site with multi-versioning via `mike`.

## Contributing

See [./CONTRIBUTING.md](./CONTRIBUTING.md)

## How versioning works

The site uses [mike](https://github.com/jimporter/mike) to maintain multiple documentation versions on the `gh-pages` branch. Each version is a self-contained snapshot.

**Aliases:**

- `latest` -- points to the most recent stable release (currently `1.3.x`)
- `dev` -- built nightly from `main`, contains unreleased content

**Branching model:**

- `main` -- all multirepo `import_url` refs point to `branch=main`. Merges to `main` auto-deploy the `dev` version.
- Release branches (e.g. `v1.3.x`) -- created for each stable release. The `import_url` refs are updated to point at specific release branches or tags for each component repo.

**Component ref patterns per release:**

Not all repos follow the same convention. When preparing a release branch, you need to look up the correct ref for each component:

| Component | Ref style | Example (v1.3.x) |
|-|-|-|
| `kuadrant-operator` | Release branch | `release-v1.3` |
| `authorino` | Tag | `v0.23.0` |
| `dns-operator` | Tag or release branch | `v0.15.0` |
| `architecture` | Always `main` | `main` |
| `developer-portal-controller` | TBD (new) | `main` |
| `kuadrant-backstage-plugin` | TBD (new) | `main` |
| `mcp-gateway` | TBD (new) | `main` |

## Running locally

### Prerequisites

Install [uv](https://github.com/astral-sh/uv) and [asciidoctor](https://asciidoctor.org/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS
brew install asciidoctor

# Linux
gem install asciidoctor
```

### Setup and serve

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
mkdocs serve -s
```

Docs will be at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Using Docker/Podman

```bash
docker run \
  -v "$(pwd):/docs" \
  -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" \
  -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
  -p 8000:8000 quay.io/kuadrant/docs.kuadrant.io:latest \
  "mkdocs serve -s -a 0.0.0.0:8000"
```

### Multi-versioned docs (from gh-pages)

```bash
mike serve
```

This serves the built versions from the `gh-pages` branch, not your working tree. For day-to-day development, use `mkdocs serve -s`.

## AsciiDoc support

Both Markdown (`.md`) and AsciiDoc (`.adoc`) files are supported via the [mkdocs-asciidoctor-backend](https://github.com/aireilly/mkdocs-asciidoctor-backend) plugin.

To add an AsciiDoc page, create a `.adoc` file in `docs/` and add it to the `nav` section in `mkdocs.yml`. See `docs/install-helm.adoc` for an example.

## Releases

### Creating a stable release

1. Create a release branch from `main` (e.g. `git checkout -b v1.4.x`).
2. Update `mkdocs.yml` on the release branch:
   - Change each `import_url` to point at the correct release branch or tag for that component (see table above).
   - Update the `edit_uri` to match the release ref where appropriate.
3. Update the version default in `mkdocs.yml`:
   ```yaml
   extra:
     version:
       provider: mike
       default:
         - 1.4.x
         - latest
   ```
4. Build and verify: `mkdocs build -s`
5. Deploy with the `latest` alias:
   ```bash
   mike deploy --update-aliases 1.4.x latest --push
   ```
6. Set as default:
   ```bash
   mike set-default 1.4.x --push
   ```

### Re-deploying a version

Use the GitHub Actions workflow: **Actions > Re-deploy via mike**. For the nightly `dev` build, this runs automatically at midnight UTC.

For manual re-deploys, specify the version and source branch in the workflow inputs.

### Common mike commands

```bash
mike list                                          # list deployed versions
mike deploy 1.4.x -t "1.4.x" --push               # deploy a version
mike deploy --update-aliases 1.4.x latest --push    # deploy with alias
mike set-default 1.4.x --push                       # set default version
mike delete 1.4.x --push                            # delete a version
```

## CI/CD

| Workflow | Trigger | What it does |
|-|-|-|
| `build.yaml` | PR, merge to `main` | Validates PRs with `mkdocs build -s`. On merge, deploys `dev` via mike. |
| `mike-redeploy.yaml` | Nightly (midnight UTC), manual | Re-deploys a version. Nightly rebuilds `dev` from `main`. |

## Building the Docker image

```bash
# single architecture
docker build -t quay.io/kuadrant/docs.kuadrant.io:latest .

# multi-architecture (amd64 + arm64)
docker buildx create --name multiarch --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t quay.io/kuadrant/docs.kuadrant.io:latest \
  --push .
```

Requires Docker Buildx and authentication to quay.io.
