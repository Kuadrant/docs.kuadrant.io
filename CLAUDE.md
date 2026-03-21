# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the documentation website for Kuadrant, built with MkDocs and Material theme. The site uses the `mkdocs-multirepo-plugin` to aggregate documentation from multiple Kuadrant repositories into a single unified documentation site.

## Key Commands

### Local Development
```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r pyproject.toml

# Serve docs locally (port 8000)
mkdocs serve -s

# Serve multi-versioned docs from gh-pages branch
mike serve

# Build docs
mkdocs build -s
```

### Package Management
The project uses `uv` for fast dependency management:
- Dependencies are defined in `pyproject.toml`
- No `requirements.txt` file (removed in favor of pyproject.toml)
- CI/CD uses `uv` with caching based on pyproject.toml changes
- Docker builds use `uv` with virtual environments

### Docker/Podman Development
```bash
# Run docs server locally
docker run -v "$(pwd):/docs" -p 8000:8000 quay.io/kuadrant/docs.kuadrant.io:latest "mkdocs serve -s -a 0.0.0.0:8000"

# Build docs using Dockerfile
docker build -t kuadrant-docs -f Dockerfile .
docker run -v "$(pwd):/docs" -p 8001:8001 kuadrant-docs "mkdocs serve -s -a 0.0.0.0:8001"
```

### Version Management
```bash
# Deploy a new version (requires gh-pages branch checked out locally)
mike deploy <version> -t "<title>"

# Set default version
mike set-default <version>

# List versions
mike list
```

### Validation
```bash
# Validate and generate explicit imports for multirepo plugin
python validate_imports.py <mkdocs.yml> [<mkdocs.yml>]
```

## Architecture & Key Files

### Core Configuration
- **`mkdocs.yml`**: Main site configuration defining navigation, theme, plugins, and multi-repo imports
- **`pyproject.toml`**: Python project configuration and dependencies (MkDocs, Material theme, mike, multirepo plugin)
- **`Dockerfile`**: Container setup using Red Hat UBI9 Python 3.9 image with uv for fast dependency installation

### Multi-Repository Structure
The site imports documentation from:
- `kuadrant-operator`: Core Kuadrant components and policies
- `authorino`: AuthN/AuthZ documentation
- `architecture`: Architecture documentation and RFCs
- `dns-operator`: DNS provider integrations

Imports are defined in `mkdocs.yml` under the `multirepo` plugin configuration with branch/tag specifications.

### Documentation Organization
Following the Diátaxis framework:
- **Concepts**: Explanations and architecture overviews
- **APIs & Reference**: Technical specifications for Kuadrant policies (AuthPolicy, RateLimitPolicy, DNSPolicy, TLSPolicy)
- **Tutorials**: Step-by-step learning guides
- **Guides**: Task-oriented how-to documentation

### Style Guidelines
- Follow `style_guide.md` for writing standards:
  - Use second person ("you"), active voice, present tense
  - Keep language simple (8th grade level)
  - Use sentence case for headings
  - Code blocks must specify language
  - Environment variables use `SCREAMING_SNAKE_CASE`

### CI/CD Workflows
- **build.yaml**: Main CI that validates PRs and deploys to `dev` on main branch merges
  - Uses `astral-sh/setup-uv@v4` action with caching based on pyproject.toml
  - Installs dependencies with `uv pip install --system -r pyproject.toml`
- **mike-redeploy.yaml**: Manual re-deployment of specific versions
  - Also uses uv for dependency installation
- **broken-links-checker.yml**: Validates documentation links
- **netlify.toml**: Netlify deployment configuration using uv

## Development Tips

### Working with Multi-Repo Plugin
- External content is imported into `_multirepo/` (gitignored)
- Use `!import` statements in nav to include external docs
- Run `validate_imports.py` to convert glob patterns to explicit imports

### Adding New Documentation
1. For local docs: Add markdown files in appropriate directories
2. For external docs: Add import configuration in `mkdocs.yml` under `multirepo.repos`
3. Update navigation in `mkdocs.yml` to include new content

### Deploying Changes
- PRs are validated with `mkdocs build -s`
- Merges to main automatically deploy to `dev` version
- Tagged releases should be deployed using `mike deploy`

### Creating Markdown Packs
Generate a complete markdown pack of all documentation for MCP ingestion:
```bash
make markdown-pack  # Fetches from source repos
# or
python fetch_markdown_pack.py
```
This creates a `markdown-pack/` directory with all markdown files from configured repos.

## Recent Project Updates

### Migration to uv Package Manager (January 2025)
The project has been migrated from pip to uv for faster dependency management:
- **Removed**: `requirements.txt` (replaced by pyproject.toml)
- **Added**: `pyproject.toml` with all dependencies
- **Updated**: All CI/CD workflows use `astral-sh/setup-uv@v4` action
- **Docker**: Uses uv with virtual environments for dependency installation
- **Netlify**: Build command updated to install and use uv

### Markdown Pack Feature (January 2025)
Added capability to create markdown packs for MCP server ingestion:
- **`fetch_markdown_pack.py`**: Script that clones repos and extracts markdown files
- **`make markdown-pack`**: Makefile target to generate packs
- **Output**: Creates `markdown-pack/` with all docs organized by source repo
- **Manifest**: Includes `manifest.json` with metadata about all files
- **Use cases**: MCP ingestion, offline browsing, documentation analysis

### Key Files Added/Modified:
- `pyproject.toml`: Python project configuration with dependencies
- `fetch_markdown_pack.py`: Markdown pack generation script
- `Makefile`: Build automation with serve, build, and pack targets
- `.gitignore`: Added markdown-pack/ directory