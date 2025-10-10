#!/usr/bin/env python3
"""
prepare stable release branch for kuadrant docs

this script automates the manual steps described in the README for creating a stable release:
1. fetches latest tags from component repositories
2. creates a release branch
3. updates mkdocs.yml with specific git refs instead of branch=main
4. updates the version default
5. deploys with mike to gh-pages branch
6. sets default version

usage: python prepare_release.py <version>
example: python prepare_release.py 1.0.x --deploy
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, capture_output=True):
    """run a shell command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture_output,
        text=True,
        cwd=cwd
    )
    if result.returncode != 0:
        print(f"error running: {cmd}")
        if capture_output:
            print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip() if capture_output else None


def fetch_latest_tag(repo_url, version_prefix=None):
    """
    fetch the latest tag from a git repository

    args:
        repo_url: github repo url (e.g., https://github.com/kuadrant/kuadrant-operator)
        version_prefix: optional version prefix to filter tags (e.g., 'v0.10')
    """
    # clone to a temp location or use ls-remote
    cmd = f"git ls-remote --tags --sort=-v:refname {repo_url}"
    output = run_command(cmd)

    # parse tags from output
    # format is: <commit_hash>\trefs/tags/<tag_name>
    tags = []
    for line in output.split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        ref = parts[1]
        # skip ^{} refs (annotated tag references)
        if ref.endswith('^{}'):
            continue
        tag = ref.replace('refs/tags/', '')
        tags.append(tag)

    if not tags:
        print(f"warning: no tags found for {repo_url}")
        return None

    # filter by version prefix if provided
    if version_prefix:
        filtered = [t for t in tags if t.startswith(version_prefix)]
        if filtered:
            tags = filtered

    return tags[0]


def update_mkdocs_yml(version, component_tags):
    """
    update mkdocs.yml with:
    1. specific tags instead of branch=main
    2. version default
    """
    mkdocs_path = Path('mkdocs.yml')
    content = mkdocs_path.read_text()

    # update each component's import_url
    for component, tag in component_tags.items():
        # pattern: import_url: https://github.com/kuadrant/<component>?...&branch=main
        pattern = f"(import_url: https://github.com/kuadrant/{component}\\?[^&]*&branch=)main"
        replacement = f"\\1{tag}"
        content = re.sub(pattern, replacement, content)
        print(f"  {component}: main -> {tag}")

    # update version default
    # find the extra.version.default section and update it
    version_pattern = r"(extra:\s+version:\s+provider: mike\s+default:\s+- )latest"
    version_replacement = r"\g<1>" + version + "\n      - latest"
    content = re.sub(version_pattern, version_replacement, content)
    print(f"  version default: latest -> {version}, latest")

    mkdocs_path.write_text(content)


def main():
    parser = argparse.ArgumentParser(
        description="prepare a stable release branch for kuadrant docs"
    )
    parser.add_argument(
        "version",
        help="version to release (e.g., 1.0.x, 0.10.0)"
    )
    parser.add_argument(
        "--version-prefix",
        help="filter component tags by version prefix (e.g., v0.10)",
        default=None
    )
    parser.add_argument(
        "--skip-branch",
        action="store_true",
        help="skip creating the release branch (useful for testing)"
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="deploy with mike after updating files"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="push to remote after deployment (only with --deploy)"
    )
    parser.add_argument(
        "--kuadrant-operator-tag",
        help="override tag for kuadrant-operator",
        default=None
    )
    parser.add_argument(
        "--authorino-tag",
        help="override tag for authorino",
        default=None
    )
    parser.add_argument(
        "--architecture-tag",
        help="override tag for architecture",
        default=None
    )
    parser.add_argument(
        "--dns-operator-tag",
        help="override tag for dns-operator",
        default=None
    )

    args = parser.parse_args()

    # check we're in the right directory
    if not Path('mkdocs.yml').exists():
        print("error: mkdocs.yml not found. run this script from the repo root.")
        sys.exit(1)

    # check we're on main or a release branch
    current_branch = run_command("git branch --show-current")
    expected_branch = f"v{args.version}"

    if current_branch != "main" and current_branch != expected_branch:
        print(f"warning: currently on branch '{current_branch}', expected 'main' or '{expected_branch}'")
        response = input("continue anyway? [y/N]: ")
        if response.lower() != 'y':
            sys.exit(1)

    # check for modified/staged files (ignore untracked)
    result = subprocess.run(
        "git status --porcelain | grep -E '^[MADRCU]'",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        print("error: working directory has uncommitted changes. commit or stash changes first.")
        print(result.stdout)
        sys.exit(1)

    print(f"preparing release {args.version}...")

    # define component repositories
    components = {
        'kuadrant-operator': 'https://github.com/kuadrant/kuadrant-operator',
        'authorino': 'https://github.com/kuadrant/authorino',
        'architecture': 'https://github.com/kuadrant/architecture',
        'dns-operator': 'https://github.com/kuadrant/dns-operator',
    }

    # fetch latest tags for each component
    print("\nfetching latest tags...")
    component_tags = {}

    for component, repo_url in components.items():
        # check for override
        override_arg = f"{component.replace('-', '_')}_tag"
        override = getattr(args, override_arg, None)

        if override:
            tag = override
            print(f"  {component}: {tag} (override)")
        else:
            tag = fetch_latest_tag(repo_url, args.version_prefix)
            if tag:
                print(f"  {component}: {tag}")
            else:
                print(f"  {component}: no tag found, keeping main")
                tag = "main"

        component_tags[component] = tag

    # create release branch if needed
    branch_name = f"v{args.version}"
    if not args.skip_branch:
        if current_branch == branch_name:
            print(f"\nalready on release branch: {branch_name}")
        else:
            print(f"\ncreating release branch: {branch_name}")
            run_command(f"git checkout -b {branch_name}")
    else:
        print("\nskipping branch creation (--skip-branch)")

    # update mkdocs.yml
    print("\nupdating mkdocs.yml...")
    update_mkdocs_yml(args.version, component_tags)

    # deploy with mike if requested
    if args.deploy:
        print(f"\ndeploying with mike...")

        # check if we need to activate venv
        venv_activate = ""
        if Path('.venv/bin/activate').exists():
            venv_activate = "source .venv/bin/activate && "

        # build push flag
        push_flag = "--push" if args.push else ""

        # deploy with aliases
        print(f"  running: mike deploy --update-aliases {args.version} latest {push_flag}")
        deploy_cmd = f"{venv_activate}mike deploy --update-aliases {args.version} latest --allow-empty {push_flag}"
        run_command(deploy_cmd, capture_output=False)

        # set default
        print(f"  running: mike set-default {args.version} {push_flag}")
        default_cmd = f"{venv_activate}mike set-default {args.version} --allow-empty {push_flag}"
        run_command(default_cmd, capture_output=False)

        print(f"\ndeployment complete!")

        if args.push:
            print(f"\nnext steps:")
            print(f"1. tag the repo: git tag {args.version} && git push <upstream> --tags")
        else:
            print(f"\nnext steps:")
            print(f"1. review gh-pages branch: git log gh-pages")
            print(f"2. test with: mike serve")
            print(f"3. when ready, push manually: git push origin gh-pages")
            print(f"4. tag the repo: git tag {args.version} && git push <upstream> --tags")
    else:
        print(f"\nrelease preparation complete!")
        print(f"\nnext steps:")
        print(f"1. review changes: git diff mkdocs.yml")
        print(f"2. test locally: mkdocs serve -s")
        print(f"3. when ready to deploy:")
        print(f"   python3 prepare_release.py {args.version} --deploy [--push]")
        print(f"   or manually:")
        print(f"   mike deploy --update-aliases {args.version} latest [--push]")
        print(f"   mike set-default {args.version} [--push]")
        print(f"4. tag the repo: git tag {args.version} && git push <upstream> --tags")


if __name__ == '__main__':
    main()
