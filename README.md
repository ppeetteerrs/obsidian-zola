# Obsidian-Zola

This repo contains an easy-to-use (read: simplistic) solution for converting an Obsidian Personal Knowledge Management System (read: bunch of random Markdowns) into a Zola site.

Disclaimer: This repo is forked from the [Adidoks](https://github.com/aaranxu/adidoks) theme. However, several changes are made to alter / improve the use experience.

## Usage

**Step 1: Check Obsidian Settings**
- Set `Settings => Files & Links => New link format`to Relative path to file
- Set `Settings => Files & Links => USe [[Wikilinks]]` to off
- Change any existing Wikilinks / Markdown links to relative Markdown links

**Step 2: Setup Netlify**
- Turn your Obsidian vault folder into a Git repository
- Create a Netlify site pointing to that Git repository

**Step 3: Edit `netlify.toml`**
- Create `netlify.toml` in your Obsidian vault folder
- Copy the content from `netlify.example.toml` in this repo and replace the placeholders

**Step 4: You'reDone!**
Push your changes and enjoy your new site!

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