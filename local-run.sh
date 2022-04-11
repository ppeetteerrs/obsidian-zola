#!/bin/bash

mkdir -p content/docs

bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds $(cat .data_path) content/docs

export SITE_URL=local
export REPO_URL=local
export LOCAL=true

python convert.py

zola serve