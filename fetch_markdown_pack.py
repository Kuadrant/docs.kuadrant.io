#!/usr/bin/env python3
"""
Fetch markdown files directly from source repositories for MCP ingestion.
This bypasses the mkdocs build process and gets the raw markdown files.
"""

import os
import yaml
import shutil
import subprocess
import json
import tempfile
from pathlib import Path
from datetime import datetime
import urllib.parse

def load_mkdocs_config():
    """Load and parse mkdocs.yml"""
    with open('mkdocs.yml', 'r') as f:
        # Use unsafe loader to handle Python object references
        return yaml.load(f, Loader=yaml.UnsafeLoader)

def parse_import_url(import_url):
    """Parse the import URL to extract repo and branch info"""
    # Example: https://github.com/kuadrant/kuadrant-operator?edit_uri=/blob/main/&branch=main
    parts = urllib.parse.urlparse(import_url)
    
    # Extract base repo URL
    repo_url = f"{parts.scheme}://{parts.netloc}{parts.path.split('?')[0]}"
    
    # Extract branch from query params
    query_params = urllib.parse.parse_qs(parts.query)
    branch = query_params.get('branch', ['main'])[0]
    
    return repo_url, branch

def clone_repo(repo_url, branch, temp_dir):
    """Clone a repository to a temporary directory"""
    repo_name = repo_url.split('/')[-1]
    clone_path = Path(temp_dir) / repo_name
    
    print(f"  Cloning {repo_url} (branch: {branch})...")
    
    # Clone with depth=1 for speed
    result = subprocess.run(
        ['git', 'clone', '--depth', '1', '--branch', branch, repo_url, str(clone_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"  Error cloning: {result.stderr}")
        return None
    
    return clone_path

def copy_imported_files(repo_path, imports, output_dir):
    """Copy only the imported files specified in mkdocs.yml"""
    copied_files = []
    
    for import_path in imports:
        # Handle glob patterns
        if '*' in import_path:
            # Convert glob pattern to Path glob
            if import_path.startswith('/'):
                import_path = import_path[1:]
            
            matching_files = list(repo_path.glob(import_path))
            for file_path in matching_files:
                if file_path.is_file():
                    rel_path = file_path.relative_to(repo_path)
                    dest_path = output_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    copied_files.append(str(rel_path))
        else:
            # Handle specific file
            if import_path.startswith('/'):
                import_path = import_path[1:]
            
            src_path = repo_path / import_path
            if src_path.exists() and src_path.is_file():
                dest_path = output_dir / import_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
                copied_files.append(import_path)
    
    return copied_files

def extract_multirepo_sources(config):
    """Extract all multi-repo sources from config"""
    sources = []
    
    multirepo_config = None
    for plugin in config.get('plugins', []):
        if isinstance(plugin, dict) and 'multirepo' in plugin:
            multirepo_config = plugin['multirepo']
            break
    
    if not multirepo_config:
        print("No multirepo plugin found in mkdocs.yml")
        return sources
    
    for repo in multirepo_config.get('nav_repos', []):
        sources.append({
            'name': repo['name'],
            'import_url': repo['import_url'],
            'imports': repo.get('imports', [])
        })
    
    return sources

def main():
    """Main function"""
    print("Fetching markdown pack from source repositories...")
    
    # Load config
    config = load_mkdocs_config()
    sources = extract_multirepo_sources(config)
    
    if not sources:
        print("No multi-repo sources found")
        return
    
    # Create output directory
    output_dir = Path('markdown-pack')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    
    # Create manifest
    manifest = {
        'created': datetime.now().isoformat(),
        'sources': [],
        'files': []
    }
    
    # Create a temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nUsing temp directory: {temp_dir}")
        
        # Process each repository
        for source in sources:
            repo_name = source['name']
            print(f"\nProcessing {repo_name}...")
            
            # Parse import URL
            repo_url, branch = parse_import_url(source['import_url'])
            
            # Clone repository
            repo_path = clone_repo(repo_url, branch, temp_dir)
            if not repo_path:
                continue
            
            # Create output directory for this repo
            repo_output = output_dir / repo_name
            repo_output.mkdir(exist_ok=True)
            
            # Copy imported files
            copied_files = copy_imported_files(
                repo_path,
                source['imports'],
                repo_output
            )
            
            print(f"  Copied {len(copied_files)} files")
            
            # Add to manifest
            manifest['sources'].append({
                'name': repo_name,
                'url': repo_url,
                'branch': branch,
                'file_count': len(copied_files)
            })
            
            for file_path in copied_files:
                file_full_path = repo_output / file_path
                if file_full_path.exists():
                    manifest['files'].append({
                        'source': repo_name,
                        'path': file_path,
                        'type': 'markdown' if file_full_path.suffix == '.md' else 'asset',
                        'size': file_full_path.stat().st_size
                    })
    
    # Also copy local docs
    local_docs = Path('docs')
    if local_docs.exists():
        print("\nProcessing local docs...")
        local_output = output_dir / 'local'
        local_output.mkdir(exist_ok=True)
        
        file_count = 0
        for file_path in local_docs.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.md', '.png', '.jpg', '.jpeg', '.gif', '.svg']:
                rel_path = file_path.relative_to(local_docs)
                dest_path = local_output / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_path)
                file_count += 1
                
                manifest['files'].append({
                    'source': 'local',
                    'path': str(rel_path),
                    'type': 'markdown' if file_path.suffix == '.md' else 'asset',
                    'size': file_path.stat().st_size
                })
        
        print(f"  Copied {file_count} files from local docs")
        
        manifest['sources'].append({
            'name': 'local',
            'url': 'local',
            'branch': 'local',
            'file_count': file_count
        })
    
    # Write manifest
    manifest_path = output_dir / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # Create README
    readme_path = output_dir / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(f"""# Kuadrant Documentation Pack

This is a markdown pack containing all documentation from the Kuadrant multi-repo setup.
Generated on: {manifest['created']}

## Contents

""")
        for source in manifest['sources']:
            f.write(f"- **{source['name']}**: {source['file_count']} files from `{source.get('branch', 'main')}` branch\n")
        
        f.write(f"\nTotal files: {len(manifest['files'])}\n")
        f.write("""
## Usage

This pack can be used for:
- Ingesting into MCP (Model Context Protocol) servers
- Offline documentation browsing
- Documentation analysis and processing
- AI/LLM training or context

## Structure

Each repository's documentation is in its own directory:
```
markdown-pack/
├── README.md
├── manifest.json
├── kuadrant-operator/
│   ├── doc/
│   └── ...
├── authorino/
│   ├── docs/
│   └── ...
├── architecture/
│   └── docs/
├── dns-operator/
│   └── docs/
└── local/
    └── ...
```

## Manifest

The `manifest.json` file contains:
- Creation timestamp
- List of all sources with their URLs and branches
- Complete file listing with paths and sizes
""")
    
    print(f"\n✅ Markdown pack created in '{output_dir}'")
    print(f"   Total files: {len(manifest['files'])}")
    print(f"   Manifest: {output_dir}/manifest.json")

if __name__ == '__main__':
    main()