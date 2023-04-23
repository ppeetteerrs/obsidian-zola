#!/bin/bash

pip install python-slugify

# Avoid copying over netlify.toml (will ebe exposed to public API)
echo "netlify.toml" >>__obsidian/.gitignore

# Avoid uploading private files
IFS=',' read -r -a ignore_directories <<< "$IGNORE_DIRECTORIES"
for file in "${ignore_directories[@]}"; do
  echo "$file" >> __obsidian/.gitignore
done

# Sync Zola template contents
rsync -a __site/zola/ __site/build
rsync -a __site/content/ __site/build/content

# Use obsidian-export to export markdown content from obsidian
mkdir -p __site/build/content/docs __site/build/__docs
if [ -z "$STRICT_LINE_BREAKS" ]; then
	__site/bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds __obsidian __site/build/__docs
else
	__site/bin/obsidian-export --frontmatter=never --no-recursive-embeds __obsidian __site/build/__docs
fi

# Run conversion script
python3 __site/convert.py

# Build Zola site
zola --root __site/build build --output-dir public
