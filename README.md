# Kuadrant Docs

## Installing mkdocs
`pip install mkdocs`

And dependencies
`pip install -r requirements.txt`


## Running Locally
`mkdocs serve -s`

The docs should then be available locally from http://127.0.0.1:8000/

**Note:** `mkdocs` will automatically clone component repositories as configured via `mkdocs.yml`.

## Building
`mkdocs build -s`

Outputs static content to `site`.

## `mike`
We use `mike` for multi-versioned docs. It's quite straight-forward: it works by adding new commits to the `gh-pages` branch each time you run `mike deploy`. It takes care of setting up the aliases, and leaves previously "deployed" docs untouched, in their old folders. These old deployments shouldn't be touched, but can be re-built if necessary.

It  Some useful commands:

List releases:

`mike list`

Build a new release, with a custom title:

`mike deploy 0.7.0 -t "0.7.0 (dev)"`

Delete a release:

`mike delete 0.7.0`

Run a multi-version release:

`mike serve -S`

## Releases

Dev releases from main will always be deployed to "x.x.x (dev)" as a fast channel. The `latest` docs version will always be a known, stable release. The version picker defaults to the latest stable release - newer docs can be found by looking at the latest dev release.

Stable releases should be tagged (e.g. `git tag 0.6.1`).

## Deploying
This is deployed via GitHub Pages, on merge to `main`.

If you need to re-trigger a deployment from main for any reason, manually run `Actions > ci > Run Workflow`:

![alt text](docs/assets/images/deploy.png)

This will build a docs bundle, and then trigger the `pages-build-deployment` action afterwards to push changes to the `gh-pages` branch.

