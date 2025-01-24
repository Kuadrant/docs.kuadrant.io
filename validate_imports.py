# Helper script to generate explicit imports for the multirepo plugin from the nav
# Note: this will not find certain kinds of links, e.g. images or links between docs - so you'll still need to do a bit of manual work to generate imports.
# The list if imports it produces will not be exhaustive. Re run `mkdocs -s` to find other, missing imports

import yaml

def generate_explicit_nav_repos(mkdocs_file):
    with open(mkdocs_file, 'r') as f:
        raw_content = f.read()

    # Preprocess to remove problematic syntax (e.g., !!python/name)
    sanitized_content = clean(raw_content)
    config = yaml.safe_load(sanitized_content)

    # Extract files from nav
    nav_files = set(extract_files_from_nav(config['nav']))

    # Build new multirepo imports
    explicit_imports = generate_imports(config['plugins'], nav_files)

    print("Updated nav_repos:")
    print(yaml.dump(explicit_imports, default_flow_style=False, sort_keys=False))

def clean(content):
    return "\n".join([line for line in content.splitlines() if '!!python/name:' not in line])

def extract_files_from_nav(nav):
    files = []
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    files.extend(extract_files_from_nav(value))
                else:
                    files.append(value)
        else:
            files.append(item)
    return files

def generate_imports(plugins, nav_files):
    new_imports = []
    for plugin in plugins:
        if isinstance(plugin, dict) and 'multirepo' in plugin:
            for repo in plugin['multirepo']['nav_repos']:
                repo_name = repo['name']
                repo_import_url = repo['import_url']
                repo_explicit_imports = []

                for pattern in repo['imports']:
                    matching_files = match_files_to_pattern(nav_files, pattern, repo_name)

                    repo_explicit_imports.extend(
                        add_leading_slash(remove_repo_name_prefix(matching_files, repo_name))
                    )

                # Deduplicate imports (may be used multiple times in nav)
                repo_explicit_imports = sorted(set(repo_explicit_imports))

                new_imports.append({
                    'name': repo_name,
                    'import_url': repo_import_url,
                    'imports': repo_explicit_imports,
                })
    return new_imports

def match_files_to_pattern(nav_files, pattern, repo_name):
    base_path = f"{repo_name}/"
    if pattern.startswith('/'):
        pattern = pattern[1:]  # Remove leading slash
    if '*' in pattern or '?' in pattern:
        # Handle glob patterns
        prefix = base_path + pattern.split('*')[0]
        return {file for file in nav_files if file.startswith(prefix)}
    else:
        # Handle exact matches
        expected_path = base_path + pattern.lstrip('/')
        return {file for file in nav_files if file == expected_path}

def remove_repo_name_prefix(files, repo_name):
    # Remove the repo name prefix from file paths
    prefix = f"{repo_name}/"
    return [file[len(prefix):] for file in files if file.startswith(prefix)]

def add_leading_slash(files):
    return [f"/{file}" if not file.startswith("/") else file for file in files]

# Run
generate_explicit_nav_repos('mkdocs.yml')
