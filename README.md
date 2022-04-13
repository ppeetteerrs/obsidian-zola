# obsidian-zola

![](https://img.shields.io/github/v/release/ppeetteerrs/obsidian-zola)
![](https://img.shields.io/github/issues-closed-raw/ppeetteerrs/obsidian-zola)
![](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=today%27s%20views&query=%24.datasets%5B1%5D.values%5B%28%40.length-1%29%5D&url=https%3A%2F%2Fyhype.me%2Fapi%2Fchart%2Frepository_views_count_chart_controller%3FrepositoryNodeId%3DR_kgDOGpHp4A)

A free (but better?) alternative to Obsidian Publish.

> This repo contains an easy-to-use (read: simplistic) solution for converting an Obsidian Personal Knowledge Management System (read: bunch of random Markdowns) into a Zola site.

Credits: This repo was forked from [Adidoks](https://github.com/aaranxu/adidoks).

# Announcements
**v1.0.0 Big Release**
- Graph view is now supported! I assume this is a highly sought-after feature, hence it would be turned on by default 🙂.
- URLs are now slugified by deafult (to adhere to best practices)! This will change the links to some pages. For those who wish to keep your shared links valid, please disable slugify in `netlify.toml`. Sorry for the inconvenience 🙇.
- Shameless promotion 😳. Sorry for adding a `Powered by obsidian-zola` line on your home page. But I believe most people who use this repo think that it should be made known to those who need it. I don't make any 💰 from this anyways.
- Markdown link parsing bug fixes.
- Major refactoring. Everything is typed and commented and properly wrapped in classes. It should be much more maintainable and forkable now 🍴.
- Local development setup (on WSL) is provided. Just provide a `.data_path` that points to your Obsidian folder, install the dependencies and run `./local-run.sh`.


# Setup

**Step 1: Setup Netlify**
- Turn your Obsidian vault folder into a Git repository
- Create a Netlify site pointing to that Git repository

**Step 2: Edit `netlify.toml`**
- Create `netlify.toml` in your Obsidian vault folder
- Copy the content from `netlify.example.toml` in this repo and replace the appropriate settings (`SITE_URL`, `REPO_URL` and `LANDING_PAGE` cannot be left empty). 

**Step 3: You're Done 🎉!**
- Push your changes and get ready to become famous!

**Step 4: Issues & Feature Requests**
- If you encounter any issues, just post in the `Issues` tab. It would be good to include a copy of the error log found in the Netlify panel if the issue is related to deployment.
- If you have any feature request, do post an issue also. However, please this repo is intended as a one-file setup. Advanced features / detailed configurability will not be supported unless it is wanted by most users. However, I can provide help for you to implement a fork that suits your needs 🥂.

# Example Site
The [example site](https://peteryuen.netlify.app/) shows the capabilities of `obsidian-zola`. Note that the example site uses the `dev` branch of `obsidian-zola`. If you see features that are available in the example site but are not available in the main branch yet, consider trying out the `dev` (unstable) branch. Exact method can be referenced from the [example repo's](https://github.com/ppeetteerrs/obsidian-pkm) `netlify.toml`.

# Features 

**Disclaimer**

> This tool is made for people who use Obsidian as a simple and efficient note-taking app (or PKM). If you configured your Obsidian with plenty of fancy shortcodes, plugins and Obsidian-specific syntax, this tool would not (and does not intend) to support those features.

**Supported**
- Knowledge graph (you can also treat it as backlinks)
- LaTEX (powered by `KaTEX`, bye MathJAX fans 👋)
- Partial string search (powered by `elasticlunr`)
- Syntax highlighting
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
