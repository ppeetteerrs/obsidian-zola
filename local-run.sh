#!/bin/bash

rm -rf build
rsync -avh zola/ build
rsync -avh content/ build/content

mkdir -p build/content/docs

bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds $(cat .data_path) build/content/docs

export SITE_URL=local
export REPO_URL=local

python convert.py

zola --root=build serve