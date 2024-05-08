# Kuadrant Docs

## Installing mkdocs
`pip install mkdocs`

And dependencies
`pip install -r requirements.txt`


## Running Locally
`mkdocs serve -s`

The docs should then be available locally from http://127.0.0.1:8000/, from the current branch.

If you'd like to test multi-versioning, run locally with the `mike` equivalent:

`mike serve`

**Note:** `mkdocs` will automatically clone component repositories as configured via `mkdocs.yml`.

## Building

See `.github/workflows/build.yaml`

## `mike`
We use `mike` for multi-versioned docs. It's quite straight-forward: it works by adding new commits to the `gh-pages` branch each time you run `mike deploy`. It takes care of setting up the aliases, and leaves previously "deployed" docs untouched, in their old folders. These old deployments shouldn't be touched, but can be re-built if necessary.

Some useful commands:

List releases:

`mike list`

Build a new release, with a custom title:

`mike deploy 0.7.0 -t "0.7.0 (dev)"`

Delete a release:

`mike delete 0.7.0`

Run a multi-version release:

`mike serve -S`

## Mike aliases

We have two aliases in use:

- `latest` which should always point at the latest, stable released docs (e.g. `latest` - > `0.7.0`)
- `dev` which always points at the `HEAD` of main, for publishing unstable/pre-release docs quickly

## Releases

Dev releases from main will always be deployed to `dev` as a fast channel. The `latest` docs version will always be a known, stable release. The version picker defaults to the latest stable release - newer docs can be found by looking at the latest dev release.

Stable releases should be tagged (e.g. `git tag 0.6.1`).

### Stable releases:

A scenario:

- 0.6.1 was the stable release
- 0.7.0 has just been released, and we want to mark it as stable
- Changes on the `HEAD` of `main` will continue to flow to the `dev` release

To mark this new release as stable:

> **Note:** This is quite manual right now. It will be automated soon.

- Branch from `main`, e.g. `git checkout -b 0.7.x`
- In your release branch, e.g. `0.7.x`:
  - Update `mkdocs.yml` to update the `branch=` refs to tags for all components
  - Set latest release as default:
    - Update `mkdocs.yml` to set latest default release:
      ```yaml
      extra:
        version:
          provider: mike
          default:
            - 0.7.0
      ```
    - Update `export KUADRANT_REF=v0.7.0` in `getting-started-single-cluster.md`
    - Update the `latest` alias to point to our newest stable release:
      - `mike deploy --update-aliases 0.7.0 latest`
    - Update refs in `gh-pages` branch:
      - `mike set-default 0.7.0`
    - Update changes, push deploy:
      - `mike deploy 0.7.0 -t "0.7.0" --push`
  - Tag the repo (e.g. `git tag 0.7.0 && git push --tags <upstream-origin>`)
- Back on `main`:
    - `git checkout main`
    - Update `mkdocs.yml`:
      ```yaml
      default:
        - 0.7.0
      ```
    - `mike deploy dev -t "dev" --push`

## Re-release docs

Generally not advised given how `mike` works, but if you need to patch an existing release (in this example, `0.7.0`):

- Fetch: `git fetch --all` (need latest gh-pages branch)
- Check out the release branch:`git checkout 0.7.x`
- Make your changes
- `mike deploy 0.7.0 -t "0.7.0" --push`
- You may receive an error like:
  ```bash
  error: failed to push branch gh-pages to origin:
  To github.com:Kuadrant/docs.kuadrant.io.git
   ! [rejected]        gh-pages -> gh-pages (non-fast-forward)
  error: failed to push some refs to 'github.com:Kuadrant/docs.kuadrant.io.git'
  hint: Updates were rejected because a pushed branch tip is behind its remote
  hint: counterpart. Check out this branch and integrate the remote changes
  hint: (e.g. 'git pull ...') before pushing again.
  hint: See the 'Note about fast-forwards' in 'git push --help' for details.
  ```
- If this happens:
  - `git checkout gh-pages`
  - `git rebase upstream gh-pages` or (to reset) `git reset --hard upstream/gh-pages`
  - Re-run: `mike deploy 0.7.0 -t "0.7.0" --push`
  - Delete and re-tag


## Deploying
This is deployed via GitHub Pages, on merge to `main`.

If you need to re-trigger a deployment from main for any reason, manually run `Actions > ci > Run Workflow`:

![alt text](docs/assets/images/deploy.png)

This will build a docs bundle, and then trigger the `pages-build-deployment` action afterwards to push changes to the `gh-pages` branch.

