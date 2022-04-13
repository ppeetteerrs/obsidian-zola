#!/bin/bash

# Remove previous build and sync Zola template contents
rm -rf build
rsync -a zola/ build
rsync -a content/ build/content

# Use obsidian-export to export markdown content from obsidian
mkdir -p build/content/docs build/__docs
bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds $(cat .data_path) build/__docs

# Set required environment variables (refer to build.environment in netlify.toml)
export SITE_URL=local
export REPO_URL=local
export LANDING_PAGE=home
export SLUGIFY=

# Run conversion script
python convert.py

# Serve Zola site
zola --root=build serve