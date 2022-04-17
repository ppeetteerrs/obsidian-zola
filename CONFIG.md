# `netlify.toml` options

> Explains the effects and details of each option in `netlify.toml`'s `build.environment`.

## Required

### `SITE_URL`
URL to your netlify site.

### `REPO_URL`
GitHub repo URL where your Markdown files are hosted.

### `LANDING_PAGE`
The Markdown file to use as your landing page when home page landing button is clicked. Note that if `SLUGIFY` is turned on (default is on), you need to slugify the folder name here. E.g. if you are using `/somewhere far/some funny note.md` as landing page, enter `LANDING_PAGE=/somewhere-far/some-funny-note.md`.

## Optional

### `SITE_TITLE`
Site title on landing page. HTML, CSS, emojis supported. Default: "Someone's Second 🧠".

### `SITE_TITLE_TAB`
Site title in browser tab, leaving blank to use `SITE_TITLE`. This is for people who added HTML code in `SITE_TITLE` but want to display a clean name in the browser tab. Default: "".

### `LANDING_TITLE`
Site title on landing page. HTML, CSS, emojis supported. Default: "I love obsidian-zola! 💖.".

### `LANDING_DESCRIPTION`
Site description on landing page. HTML, CSS, emojis supported. Default: "I have nothing but intelligence.".

### `LANDING_BUTTON`
Text to display on button in home page. HTML, CSS, emojis supported. Default: "Click to steal some👆".

### `TIMEZONE`
Site Timezone. Default: "Asia/Hong_Kong". I guess now you know where I am from :)

### `SORT_BY`
How to sort your pages inside a folder ("title" or "date"). Default:  "title". Folders are sorted alphabetically, cannot change this.

### `GANALYTICS`
Google Analytics Measurement ID. Default: "".

### `SLUGIFY`
Whether to slugify URLs. Set to "" to disable (use at your own risk, filenames with special symbols might not show up correctly in the graph view). Default: "y".

### `HOME_GRAPH`
Shows knowledge graph on home page. Put "" to disable. Default: "y".

### `PAGE_GRAPH`
Shows knowledge graph on every page. Put "" to disable. Default: "y".

### `LOCAL_GRAPH`
Page graph only shows directly connected nodes. Default: "".

### `GRAPH_LINK_REPLACE`
If "y", clicking on graph link replaces current tab. Else, page is opened in new tab. Default: "".

### `STRICT_LINE_BREAKS`
Whether to use standard Markdown strict line breaks (single line breaks ignored unless followed by 2 whitespaces), or to use Obsidian-style line breaks. If "y", strict line break is used, else, Obsidian-style is used. Users who use LaTEX must set this to "y" for equations to render properly. Default: "y".

### `SIDEBAR_COLLAPSED`
Whether sidebar sections should be collapsed by default. Default: "".

## Animations
`Animate.css`, `Hover.css` and `CSShake` classes can be used in all fields where HTML + CSS are supported. Refer to example repo's setup on how to do so.


## Do Not Touch
Do not change theses:
- `PYTHON_VERSION`
- `ZOLA_VERSION`


# FAQs

## How do I exclude notes from the website?
Use a `.gitignore` file to prevent pushing private notes to a public repository.