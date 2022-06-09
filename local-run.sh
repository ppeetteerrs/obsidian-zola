#!/bin/bash

# Check for python-is-python3 installed
if ! command -v python &>/dev/null; then
	echo "It appears you do not have python-is-python3 installed"
	exit 1
fi

# Check for zola being installed
if ! command -v zola &>/dev/null; then
	echo "zola could not be found please install it from https://www.getzola.org/documentation/getting-started/installation"
	exit 1
fi

# Check for correct slugify package
PYTHON_ERROR=$(eval "python -c 'from slugify import slugify; print(slugify(\"Test String One\"))'" 2>&1)

if [[ $PYTHON_ERROR != "test-string-one" ]]; then
	if [[ $PYTHON_ERROR =~ "NameError" ]]; then
		echo "It appears you have the wrong version of slugify installed, the required pip package is python-slugify"
	else
		echo "It appears you do not have slugify installed. Install it with 'pip install python-slugify'"
	fi
	exit 1
fi

# Check for rtoml package
PYTHON_ERROR=$(eval "python -c 'import rtoml'" 2>&1)

if [[ $PYTHON_ERROR =~ "ModuleNotFoundError" ]]; then
	echo "It appears you do not have rtoml installed. Install it with 'pip install rtoml'"
	exit 1
fi

# Check that the vault got set
if [[ -z "${VAULT}" ]]; then
	if [[ -f ".vault_path" ]]; then
		export VAULT=$(cat .vault_path)
	else
		echo "Path to the obsidian vault is not set, please set the path using in the $(.vault_path) file or $VAULT env variable"
		exit 1
	fi
fi

# Pull environment variables from the vault's netlify.toml when building (by generating env.sh to be sourced)
python env.py

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
source env.sh && python convert.py && rm env.sh

# Serve Zola site
zola --root=build serve
