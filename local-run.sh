#!/bin/bash

# Set required environment variables (refer to build.environment in netlify.toml)
export SITE_URL=local
export REPO_URL=local
export LANDING_PAGE=home
export SLUGIFY=y
export HOME_GRAPH=y
export PAGE_GRAPH=y
export LOCAL_GRAPH=y
export GRAPH_LINK_REPLACE=y
export STRICT_LINE_BREAKS=y
export SIDEBAR_COLLAPSED=y

# Remove previous build and sync Zola template contents
rm -rf build
rsync -a zola/ build
rsync -a content/ build/content

# Use obsidian-export to export markdown content from obsidian
mkdir -p build/content/docs build/__docs
if [ -z "$STRICT_LINE_BREAKS" ]; then
	bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds $(cat .data_path) build/__docs
else
	bin/obsidian-export --frontmatter=never --no-recursive-embeds $(cat .data_path) build/__docs
fi

# Run conversion script
python convert.py

# Serve Zola site
zola --root=build serve
