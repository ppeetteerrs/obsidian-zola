#!/bin/bash

echo "netlify.toml" >> __obsidian/.gitignore

# Sync Zola template contents
rsync -avh __site/zola/ __site/build
rsync -avh __site/content/ __site/build/content

# Use obsidian-export to export markdown content from obsidian
mkdir -p __site/build/content/docs
__site/bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds __obsidian __site/build/content/docs

# Run conversion script
python __site/convert.py

# Build Zola site
zola --root __site/build build --output-dir public