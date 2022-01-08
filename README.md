# Obsidian-Zola

This repo contains an easy-to-use (read: simplistic) solution for converting an Obsidian Personal Knowledge Management System (read: bunch of random Markdowns) into a Zola site.

Disclaimer: This repo is forked from the [Adidoks](https://github.com/aaranxu/adidoks) theme. However, several changes are made to alter / improve the use experience.

## Usage
- Step 1: Create a git repo out of your Obsidian directory.
- Step 2: Copy `netlify.example.toml` into `<your_obsidian_dir>/netlify.toml` and change the placeholders.
- Step 3: Commit and push your changes to git repository, create a netlify site using your repo. Make sure that the `SITE_URL` in `netlify.toml` matches your actual netlify site url.
- Step 4: Enjoy your new site!

## Examples
[Example site](https://peteryuen.netlify.app/)

[Example repo](https://github.com/ppeetteerrs/obsidian-pkm)

## Features (vs the original AdiDoks)

First of all, this repo is fully customized for Obsidian PKMs. Of course you can still use it like a regular Zola theme, but it might lack some flexibility in terms of customization.

### Enhancements

**Search Function**

Partial strings are supported now. Since PKM often invole plenty of jargons and the default elasticlunr (of course) cannot do proper stemming on those words, partial string search is an absolute must when it comes to PKM searching.

**Fonts**

Changed default font to Inter for a neater interface.

Changed monospace font to Fira Code because who doesn't love font ligatures?

**KaTEX**

Updated KaTEX to latest version and loads KaTEX by default. Since who on earth builds a PKM without any LaTEX :)

**Table of Content**

Again, who wants to write a PKM page without proper TOC navigation :))

### Small Chanages

**Change Default Content**

Default footers, licenses and menu items are gone. Bye and see you never!

**Example Site Materials**

Deleted example site content and stuff to prevent a bloated repo :)