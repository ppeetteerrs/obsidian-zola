#!/bin/bash

echo "netlify.toml" >> __obsidian/.gitignore

rsync -avh __site/zola/ __site/build
rsync -avh __site/content/ __site/build/content

mkdir -p __site/build/content/docs

__site/bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds __obsidian __site/build/content/docs

python __site/convert.py

zola --root __site/build build --output-dir public