#!/bin/bash

# Path to the vault
export VAULT=""
# Check that the vault got set
if [[ -z "${VAULT}" ]]; then
  echo "Path to the obsisian vault is not set, please set the path in local-run.sh"
  exit 1
fi

# Pull environment variables from the netlify.toml when building
eval $(awk '/\[build.environment\]/{flag=1;next}/^\s*$/{flag=0} {if (flag && $1 != "#" && $1 != "") {printf("export %s=", $1)} if (flag && $1 != "#" && $1 != "") for(i=3;  i<=NF;  i++) if(i==NF) {printf("%s\n", $i)} else printf("%s ", $i)}' netlify.toml | sed 's/\r$//')

# Set the site and repo url as local since locally built
export SITE_URL=local
export REPO_URL=local

# Remove previous build and sync Zola template contents
rm -rf build
rsync -a zola/ build
rsync -a content/ build/content

# Use obsidian-export to export markdown content from obsidian
mkdir -p build/content/docs build/__docs
if [ -z "$STRICT_LINE_BREAKS" ]; then
	bin/obsidian-export --frontmatter=never --hard-linebreaks --no-recursive-embeds $VAULT build/__docs
else
	bin/obsidian-export --frontmatter=never --no-recursive-embeds $VAULT build/__docs
fi

# Run conversion script
python convert.py

# Serve Zola site
zola --root=build serve
