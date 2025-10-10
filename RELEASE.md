# Release automation

## Quick start

```bash
# prepare release (creates branch, updates files)
python3 prepare_release.py 1.3.x

# review changes
git diff mkdocs.yml

# test locally
mkdocs serve -s

# deploy to gh-pages (without pushing)
python3 prepare_release.py 1.3.x --deploy

# test multi-version docs
mike serve

# when satisfied, push
git push origin gh-pages

# tag the release
git tag 1.3.x && git push origin --tags
```

## Usage

### Basic workflow

```bash
# 1. from main branch, prepare release
python3 prepare_release.py 1.3.x
```

This will:
- fetch latest tags from all component repos
- create branch `v1.3.x`
- update mkdocs.yml with specific tags instead of `branch=main`
- update version default

### Deploy with mike

```bash
# 2. review and deploy
python3 prepare_release.py 1.3.x --deploy
```

This adds:
- runs `mike deploy --update-aliases 1.3.x latest`
- runs `mike set-default 1.3.x`
- commits to gh-pages branch locally (without pushing)

### Options

```bash
# filter component tags by version prefix
python3 prepare_release.py 1.3.x --version-prefix v1.3

# override specific component tags
python3 prepare_release.py 1.3.x \
  --kuadrant-operator-tag v1.3.0 \
  --authorino-tag v0.23.0

# deploy and push in one go (careful!)
python3 prepare_release.py 1.3.x --deploy --push

# dry run (no branch creation)
python3 prepare_release.py 1.3.x --skip-branch
```

### Re-running

If you need to update a release:

```bash
# checkout release branch
git checkout v1.3.x

# re-run with new tags
python3 prepare_release.py 1.3.x --kuadrant-operator-tag v1.3.1

# redeploy
python3 prepare_release.py 1.3.x --deploy
```

## What the script does

### Tag fetching

The script uses `git ls-remote` to fetch the latest tags from each component repository:
- kuadrant-operator
- authorino
- architecture
- dns-operator

It automatically selects the latest tag (sorted by version), or you can filter by prefix or override manually.

### File updates

Updates `mkdocs.yml`:
- replaces `branch=main` with `branch=<tag>` for each component
- adds version to `extra.version.default`

### Mike deployment

Runs mike commands to:
- deploy docs to gh-pages branch
- update 'latest' alias
- set default version

By default, changes are committed locally without pushing, so you can review before pushing.

## Manual process (original)

See README.md for the full manual process. The script automates steps 1-3 of the release process.
