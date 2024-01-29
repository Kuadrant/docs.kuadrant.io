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

## Deploying
This is deployed via GitHub Pages, on merge to `main`.

If you need to re-trigger a deployment from main for any reason, manually run `Actions > ci > Run Workflow`:

![alt text](docs/assets/images/deploy.png)

This will build a docs bundle, and then trigger the `pages-build-deployment` action afterwards to push changes to the `gh-pages` branch.

