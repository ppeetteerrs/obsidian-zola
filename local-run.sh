#!/bin/bash

# Check for python-is-python3 installed
if ! command -v python &> /dev/null
then
  echo "It appears you do not have python-is-python3 installed"
  exit 1
fi

# Check for zola being installed
if ! command -v zola &> /dev/null
then
  echo "zola could not be found please install it from https://www.getzola.org/documentation/getting-started/installation"
  exit 1
fi

# Check for correct slugify package
PYTHON_ERROR=$(eval "python -c 'from slugify import slugify; print(slugify(\"Test String One\"))'" 2>&1)

if [[ $PYTHON_ERROR != "test-string-one" ]]
then
  if [[ $PYTHON_ERROR =~ "NameError" ]]
  then
    echo "It appears you have the wrong version of slugify installed, the required pip package is python-slugify"
  else
    echo "It appears you do not have slugify installed. Install it with 'pip install python-slugify'"
  fi
  exit 1
fi

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
