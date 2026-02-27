---
description: Create a minor docs release (e.g., v1.3.x -> v1.4.x)
---

Perform a minor release of the Kuadrant documentation site. This creates a new versioned release branch and updates all multirepo import refs to point at the correct release branches/tags for each component.

The user will provide the new version (e.g. "1.4.x") and the previous version to base from (e.g. "1.3.x"). If not provided, look at mkdocs.yml `extra.version.default` to determine the current latest, and increment the minor number.

## Steps

1. **Check prerequisites:**
   - Verify `gh` CLI is installed and authenticated: `gh auth status`
   - If not installed or not authenticated, stop and tell the user to install/authenticate first
   - Check if `mkdocs` is available locally (e.g. in a venv). If not, note that docker/podman will be used instead via:
     `docker run -v "$(pwd):/docs" -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" quay.io/kuadrant/docs.kuadrant.io:latest "<command>"`
   - Set a variable to track which method to use (local or docker) for subsequent build/deploy steps

2. **Sync with upstream:**
   - `git fetch upstream`
   - Ensure local `main` is up to date with `upstream/main`
   - If behind: `git rebase upstream/main`

3. **Determine the new version:**
   - Read the current `extra.version.default` from `mkdocs.yml` on `main` to find the current latest (e.g. `1.3.x`)
   - The new version increments the minor number (e.g. `1.4.x`)
   - Confirm with the user before proceeding

4. **Look up component release refs (using `gh` CLI):**
   For each component in `mkdocs.yml` under `multirepo.nav_repos`, determine the correct git ref. The ref should match whatever branch or tag corresponds to the **latest GitHub release** for that component. Version numbers across components don't necessarily correlate -- e.g. Kuadrant v1.4 might use authorino v0.24.0 and dns-operator v0.16.0.

   For each component (except `architecture` which is always `main`), look up the latest GitHub release:
   Run: `gh api repos/kuadrant/{repo}/releases/latest --jq '.tag_name'`

   Then check whether that release tag has a corresponding branch (some repos use release branches, others just tags):
   Run: `gh api repos/kuadrant/{repo}/branches --paginate --jq '.[].name' | grep release`

   Use the release branch if one exists for that version, otherwise use the tag directly.

   Present the discovered refs to the user in a table and ask them to confirm or correct before proceeding. Format:

   | Component | Latest release | Ref to use | Type |
   |-|-|-|-|
   | kuadrant-operator | v1.4.0 | release-v1.4 | branch |
   | authorino | v0.24.0 | v0.24.0 | tag |
   | dns-operator | v0.16.0 | v0.16.0 | tag |
   | ... | ... | ... | ... |

5. **Create the release branch:**
   - `git checkout -b v{VERSION} main` (e.g. `v1.4.x`)

6. **Update mkdocs.yml on the release branch:**
   - For each component, update the `import_url` line to use the confirmed ref:
     `https://github.com/kuadrant/{repo}?edit_uri=/blob/{ref}/&branch={ref}`
   - Update `edit_uri` to match the release ref for repos that have release branches (e.g. kuadrant-operator).
     For tag-only repos (e.g. authorino), the edit_uri can stay pointing at `main` since tags are read-only.
   - Update the version default:
     ```yaml
     extra:
       version:
         provider: mike
         default:
           - {VERSION}
           - latest
     ```

7. **Build and verify:**
   - If mkdocs is available locally: `mkdocs build -s`
   - If using docker: `docker run -v "$(pwd):/docs" quay.io/kuadrant/docs.kuadrant.io:latest "mkdocs build -s"`
   - If it fails, diagnose and fix before continuing

8. **Print a summary of commands for the user to run:**
   After the build succeeds, print a copy-pasteable block of all remaining commands.
   Use the local or docker variant depending on what was detected in step 1.

   Local:
   ```
   # push the release branch to upstream (Kuadrant org)
   git push upstream v{VERSION}

   # deploy to gh-pages with the latest alias
   mike deploy --update-aliases {VERSION} latest --push --remote upstream

   # set as the default version
   mike set-default {VERSION} --push --remote upstream

   # switch back to main and update the default version
   git checkout main
   # (optionally update extra.version.default in mkdocs.yml on main to {VERSION})
   ```

   Docker:
   ```
   git push upstream v{VERSION}

   docker run -v "$(pwd):/docs" -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
     quay.io/kuadrant/docs.kuadrant.io:latest "mike deploy --update-aliases {VERSION} latest --push --remote upstream"

   docker run -v "$(pwd):/docs" -v "$HOME/.gitconfig:/opt/app-root/src/.gitconfig:ro" -v "$HOME/.ssh:/opt/app-root/src/.ssh:ro" \
     quay.io/kuadrant/docs.kuadrant.io:latest "mike set-default {VERSION} --push --remote upstream"

   git checkout main
   ```

   Only print the variant that matches the user's environment.

Important notes:
- This repo uses a fork workflow (origin = user's fork, upstream = Kuadrant org). Pushes go to upstream, not origin.
- NEVER run `git push`, `mike deploy`, or `mike set-default` commands. Only print them as instructions for the user to copy and run themselves.
- If a component ref can't be found, ask the user rather than guessing
- Some newer components (developer-portal-controller, kuadrant-backstage-plugin, mcp-gateway) may not have release branches yet -- default to `main` and flag it
- The build step is critical -- don't skip it, as missing imports will cause failures in strict mode
