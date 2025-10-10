# Release automation

## Quick start

### Via GitHub Actions (recommended)

1. go to `Actions > prepare release > Run workflow`
2. fill in the version (e.g., `1.3.x`)
3. optionally enable `deploy with mike`
4. run the workflow
5. review the diff in the workflow summary
6. if happy, run again with `push to remote` enabled
7. tag the release locally: `git tag 1.3.x && git push origin --tags`

### Via local script

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

## GitHub Actions workflow

The workflow provides all the same options as the script:

**Inputs:**
- `version` (required): version to release (e.g., `1.3.x`)
- `version_prefix`: filter component tags by prefix (e.g., `v1.3`)
- `deploy`: deploy with mike (default: false)
- `push`: push to remote - only works with deploy enabled (default: false)
- `kuadrant_operator_tag`: override kuadrant-operator tag
- `authorino_tag`: override authorino tag
- `architecture_tag`: override architecture tag
- `dns_operator_tag`: override dns-operator tag

**Workflow summary shows:**
- diff of mkdocs.yml changes
- gh-pages commits (if deploy enabled)
- artifact download with full changes (if push disabled)

**Typical workflow:**
1. run without push to preview changes
2. review diff in summary
3. run again with push enabled if satisfied

## Local script usage

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
