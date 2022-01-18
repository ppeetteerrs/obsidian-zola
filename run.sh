#!/bin/bash

echo "netlify.toml" >> __obsidian/.gitignore
mkdir __site/content/docs

wget https://github.com/zoni/obsidian-export/releases/download/v22.1.0/obsidian-export_Linux-x86_64.bin -O export.bin
chmod +x export.bin
./export.bin --frontmatter=never --hard-linebreaks --no-recursive-embeds __obsidian __site/content/docs

python __site/convert.py

zola --root __site build --output-dir public