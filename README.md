<p align="center">
  <img height="200" src="icon.png">
</p>

# obsidian-zola

![](https://img.shields.io/github/v/release/ppeetteerrs/obsidian-zola)
![](https://img.shields.io/github/issues-closed-raw/ppeetteerrs/obsidian-zola)
![](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=today%27s%20views&query=%24.datasets%5B1%5D.values%5B%28%40.length-1%29%5D&url=https%3A%2F%2Fyhype.me%2Fapi%2Fchart%2Frepository_views_count_chart_controller%3FrepositoryNodeId%3DR_kgDOGpHp4A)

A free (but better?) alternative to Obsidian Publish.

> This repo contains an easy-to-use (read: simplistic) solution for converting an Obsidian Personal Knowledge Management System (read: bunch of random Markdowns) into a Zola site.

Credits: This repo was forked from [Adidoks](https://github.com/aaranxu/adidoks).

Special Thanks: Wikilink parsing is powered by [obsidian-export](https://github.com/zoni/obsidian-export).

# Announcements

**v1.3.0 Satisfying Feature Requests! ✨**

Bug Fixes:

- Fixed some more bugs related to unconventional filenames (e.g. containing "." and other special characters)


Improvements:

- Better local test setup (see `Local Testing` below)
- Configurable root section name
- Configurable footer content

# Setup

**Step 1: Setup Netlify**

- Turn your Obsidian vault folder into a Git repository
- Create a Netlify site pointing to that Git repository

**Step 2: Edit `netlify.toml`**

- Create `netlify.toml` in your Obsidian vault folder
- Copy the content from `netlify.example.toml` in this repo and replace the appropriate settings (`SITE_URL`, `REPO_URL` and `LANDING_PAGE` cannot be left empty). 

**Step 3: You're Done 🎉!**

- Push your changes and get ready to become famous!
- Be Fancy: All text field settings in `netlify.toml` (e.g. `LANDING_TITLE`) supports HTML syntax. And I added `Animate.css` + `Hover.css` + `CSShake` for those of you who want to add a personal touch~ 

**Step 4: Issues & Feature Requests**

- If you encounter any issues, first refer to [Config+FAQ](https://github.com/ppeetteerrs/obsidian-zola/blob/main/CONFIG.md). If still unsolved, just post in the `Issues` tab. It would be good to include a copy of the error log found in the Netlify panel if the issue is related to deployment.
- If you have any feature request, do post an issue also. However, please this repo is intended as a one-file setup. Advanced features / detailed configurability will not be supported unless it is wanted by most users. However, I can provide help for you to implement a fork that suits your needs 🥂.

**Step 5: (Optional Enhancement) Auto Sitemap Submit**

To make your site more friendly to search engines, you can add a netlify plugin to automatically submit the new sitemap everytime you re-deploy the site. Just add the following to your `netlify.toml`. Remember to replace `baseUrl` with your `SITE_URL`.

```toml
[[plugins]]
package = "netlify-plugin-submit-sitemap"

[plugins.inputs]

# The base url of your site (optional, default = main URL set in Netlify)
baseUrl = "https://peteryuen.netlify.app/"

# Path to the sitemap URL (optional, default = /sitemap.xml)
sitemapPath = "/sitemap.xml"

# Time in seconds to not submit the sitemap after successful submission
ignorePeriod = 0

# Enabled providers to submit sitemap to (optional, default = 'google', 'bing', 'yandex'). Possible providers are currently only 'google', 'bing', 'yandex'.
providers = [
  "google",
  "bing",
  "yandex",
]
```

# Example Site

> Do not copy `netlify.toml` from example site, it is unstable. Please reference from `netlify.example.toml`.

The [example site](https://peteryuen.netlify.app/) shows the capabilities of `obsidian-zola`. Note that the example site uses the `dev` branch of `obsidian-zola`. If you see features that are available in the example site but are not available in the main branch yet, consider trying out the `dev` (unstable) branch. Exact method can be referenced from the [example repo's](https://github.com/ppeetteerrs/obsidian-pkm) `netlify.toml`.

# Local Testing (Ubuntu) [thanks @trwbox]

- Install zola from the instuctions on the site `https://www.getzola.org/documentation/getting-started/installation/`
- Run the following commands to install other needed dependencies `sudo apt install python-is-python3 python3-pip` and `pip3 install python-slugify rtoml` (or use `conda` / `mamba`)
- Use `git clone https://github.com/ppeetteerrs/obsidian-zola` to clone the repo to somewhere other than inside the Obsidian vault folder
- Set the path to the Obsisian vault using a `.vault_path` file or the `$VAULT` environment variable
- use `./local-run.sh` to run the site

# Features 

**Disclaimer**

> This tool is made for people who use Obsidian as a simple and efficient note-taking app (or PKM). If you configured your Obsidian with plenty of fancy shortcodes, plugins and Obsidian-specific syntax, this tool would not (and does not intend) to support those features.

**Supported**
- Knowledge graph (you can also treat it as backlinks)
- LaTEX (powered by `KaTEX`, bye MathJAX fans 👋)
- Partial string search (powered by `elasticlunr`)
- Syntax highlighting + Fira Code!
- Customizable animations
- Navigation
- Table of content
- Typical Markdown syntax
- Strikethroughs
- Tables
- Single-line footnotes (i.e. `[^1]` in the paragraph and `[^1]: xxx` later)
- Checkboxes
- Link escaping pattern: `[Slides Demo](<Slides Demo>)`

**Unsupported**

- Non-image / note embeds (e.g. videos, audio, PDF). They will be turned into links.
- Image resizing
- Highlighting text
- Comments
- Inline / Multi-line footnotes
- Mermaid Diagrams

# Gotchas
1. Do not have files with name `index.md` or `_index.md`
2. ~~Do not have files that have the same name as its subfolder (e.g. having both `.../category1.md` and `.../category1/xxx.md` is not allowed)~~ (Fixed)
3. `LANDING_PAGE` needs to be set to the slugified file name if `SLUGIFY` is turned on (e.g. to use `I am Home.md`, `LANDING_PAGE` needs to be `i-am-home`)

# WIPs / Ideas
- (Probably will do) Backlinks / Mentioned in
- (Maybe) Lottie animations?
- (Dunno) Configurable collapse icon
