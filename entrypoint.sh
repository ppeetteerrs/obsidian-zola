#!/bin/sh
if [ -f /obsidian/netlify.toml ]; then
    echo 'good luck'
    cd /obsidian-zola
    sh local-run.sh
    sleep infinity
else
    echo "netlify.toml not found in the bind mount to /obsidian"
    cd /obsidian
    cp /obsidian-zola/netlify.example.toml /obsidian/netlify.toml
    echo You should set SITE_URL to your public ip, now SITE_URL is $SITE_URL
    sed -i 's|SITE_URL = ""|SITE_URL = "'"$SITE_URL"'"|' /obsidian/netlify.toml
    cd /obsidian-zola
    sh local-run.sh
    sleep infinity
fi
