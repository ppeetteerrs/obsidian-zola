import json
import math
import os
import re
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Callable, Dict, List, Tuple
from urllib import parse as urlparse

DEFAULTS = {
    "SITE_URL": None,
    "SITE_TITLE": "I love obsidian-zol",
    "TIMEZONE": "Asia/Hong_Kong",
    "REPO_URL": None,
    "LANDING_PAGE": "home",
    "LANDING_TITLE": "I love obsidian-zola!",
    "LANDING_DESCRIPTION": "I have nothing but intelligence.",
    "LANDING_BUTTON": "Steal some of my intelligence",
    "SORT_BY": "title",
    "GANALYTICS": "",
}

ZOLA_DIR = Path(__file__).resolve().parent / "build"
DOCS_DIR = ZOLA_DIR / "content" / "docs"

# key: relative path, value: title
nodes: Dict[str, str] = {}
# from relative path, to relative path
edges: List[Tuple[str, str]] = []


def print_step(msg: str):
    print(msg.center(100, "-"))


def process_lines(path: Path, fn: Callable[[str], str]):
    content = "\n".join([fn(line.rstrip()) for line in open(path, "r").readlines()])
    open(path, "w").write(content)
    print_step(str(path))
    print(content)


def step1():
    """
    Check environment variables
    """
    print_step("CHECKING ENVIRONMENT VARIABLES")
    for item in DEFAULTS.keys():
        if item not in environ:
            def_val = DEFAULTS[item]

            if def_val is None:
                raise Exception(f"FATAL ERROR: build.environment.{item} not set!")
            else:
                print(
                    f"WARNING: build.environment.{item} not set! Defaulting to '{def_val}'."
                )
                environ[item] = def_val
        else:
            print(f"{item}: {environ[item]}")


def step2():
    """
    Substitute netlify.toml settings into config.toml and landing page
    """

    print_step("SUBSTITUTING CONFIG FILE AND LANDING PAGE")

    if "LOCAL" not in environ:

        def sub(line: str) -> str:
            for env_var in DEFAULTS.keys():
                line = line.replace(f"___{env_var}___", environ[env_var])
            return line

        process_lines(ZOLA_DIR / "config.toml", sub)
        process_lines(ZOLA_DIR / "content" / "_index.md", sub)


def step3():
    """
    Generate _index.md for each section
    """

    print_step("GENERATING _index.md")
    sections = list(sorted(DOCS_DIR.glob("**/**"), key=lambda x: str(x).lower()))
    content = None
    for idx, section in enumerate(sections):
        # Set section title as relative path to section
        title = re.sub(r"^.*?content/docs/*", "", str(section))

        # Call the root section "main"
        if title == "":
            title = "main"

        sort_by = (
            "date"
            if "SORT_BY" in environ and environ["SORT_BY"].lower() == "date"
            else "title"
        )

        # Print frontmatter to file
        content = [
            "---",
            f"title: {title}",
            "template: docs/section.html",
            f"sort_by: {sort_by}",
            f"weight: {idx}",
            "---",
        ]
        open(section / "_index.md", "w").write("\n".join(content))
    if content:
        print("\n".join(content))


def remove_frontmatters(content: List[str]) -> List[str]:
    """
    Remove obsidian-specific frontmatters
    """

    # Skip if no frontmatters
    if len(content) == 0 or not content[0].startswith("---"):
        return content

    # Search for line number where frontmatters ends
    frontmatter_end = -1
    for i, line in enumerate(content[1:]):
        if line.startswith("---"):
            frontmatter_end = i
            break

    # Return content without frontmatters
    if frontmatter_end > 0:
        return content[frontmatter_end + 2 :]

    # No frontmatters ending tag
    return content


def no_inner_link(item: str) -> bool:
    """
    Avoids regex matches that span over multiple links
    """
    return re.match(r"\[.+?\]\(\S+?\)", item) is None


def get_md_links(line: str) -> List[Tuple[str, str, str]]:
    """
    Returns entire match, title and url body for Markdown links found
    """

    return [
        (combined, title, body)
        for combined, title, body in re.findall(
            r"(\[(.+?)\]\((?!http)(\S+?)(?:\.md)(?:#\S+)?\))", line
        )
        if not no_inner_link(combined)
    ]


def get_internal_links(line: str) -> List[Tuple[str, str, str, str]]:
    """
    Returns entire match, title, url body and heading (including the # symbol) for non-HTTP links found
    """

    # (\[.+?\]): Capture [xxx] part
    # \((?!http)(.+?)(?:.md)?\): Capture (yyy) part, ensuring that link is not http and remove .md from markdown files
    # (#.+)?: Capture any heading tags after ".md"
    return [
        (combined, title, body, heading)
        for combined, title, body, heading in re.findall(
            r"(\[(.+?)\]\((?!http)(\S+?)(?:\.md)?(#\S+)?\))", line
        )
        if not no_inner_link(combined)
    ]


# Markdown links: \[(.+?)\]\((?!http)(\S+?)(?:\.md)(?:#\S+)?\)
# Non-http links


def filter_lines(file: Path, content: List[str]) -> List[str]:
    """
    1. Replace obsidian relative links to valid absolute links
    2. Double escape latex newline
    """
    global nodes, edges
    # Relative path of current file
    rel_path = re.sub(r"^.*?content/*", "/", str(file)).replace(".md", "")
    nodes[rel_path] = file.stem

    # Replace relative links
    parent_dir = Path(
        f"{file.parents[0]}".replace(str(ZOLA_DIR / "content"), "").replace(" ", "%20")
    )

    parsed_lines = []

    for line in content:

        parsed_line = line

        for combined, title, body in get_md_links(line):
            edges.append(
                tuple(
                    sorted(
                        [rel_path, urlparse.unquote(str((parent_dir / body).resolve()))]
                    )
                )
            )

        for combined, title, body, heading in get_internal_links(line):
            parsed_line = parsed_line.replace(
                combined, f"[{title}]({(parent_dir / body).resolve()}{heading})"
            )

        parsed_lines.append(parsed_line)

    # Replace ending double forward slashes (in LaTEX) to fix line breaks
    replaced_slashes = [re.sub(r"\\\\\s*$", r"\\\\\\\\", line) for line in parsed_lines]

    return replaced_slashes


def write_frontmatters(file: Path, content: List[str]) -> List[str]:
    """
    Write Zola-specific frontmatters
    """

    # Use Titlecase file name (preserving uppercase words) as title
    title = " ".join(
        [item if item[0].isupper() else item.title() for item in file.stem.split(" ")]
    )

    # Use last modified time as creation and updated time
    modified = datetime.fromtimestamp(os.path.getmtime(file))

    return [
        "---",
        f"title: {title}",
        f"date: {modified}",
        f"updated: {modified}",
        "template: docs/page.html",
        "---",
        *content,
    ]


def parse_graph():
    global nodes, edges

    # Write visualization JSON
    hash_ids = {k: i for i, k in enumerate(nodes.keys())}
    existing_edges = [
        edge for edge in set(edges) if edge[0] in hash_ids and edge[1] in hash_ids
    ]

    colors = [
        # First tier
        "#FFADAD",
        "#FFD6A5",
        "#FDFFB6",
        "#CAFFBF",
        "#9BF6FF",
        "#A0C4FF",
        "#BDB2FF",
        "#FFC6FF",
        # Second tier
        "#FBF8CC",
        "#FDE4CF",
        "#FFCFD2",
        "#F1C0E8",
        "#CFBAF0",
        "#A3C4F3",
        "#90DBF4",
        "#8EECF5",
        "#98F5E1",
        "#B9FBC0",
        # Third tier
        "#EAE4E9",
        "#FFF1E6",
        "#FDE2E4",
        "#FAD2E1",
        "#E2ECE9",
        "#BEE1E6",
        "#F0EFEB",
        "#DFE7FD",
        "#CDDAFD",
    ]

    n_colored = len(colors)

    edge_counts = {k: 0 for k in nodes.keys()}

    for i, j in existing_edges:
        edge_counts[i] += 1
        edge_counts[j] += 1

    top_nodes = {
        node_url: i
        for i, (node_url, _) in enumerate(
            list(sorted(edge_counts.items(), key=lambda k: -k[1]))[:n_colored]
        )
    }

    graph_info = {
        "nodes": [
            {
                "id": hash_ids[url],
                "label": title,
                "url": url,
                "color": colors[top_nodes[url]] if url in top_nodes else None,
                "value": math.log10(edge_counts[url] + 1) + 1,
                "opacity": 0.1,
            }
            for url, title in nodes.items()
        ],
        "edges": [
            {"from": hash_ids[edge[0]], "to": hash_ids[edge[1]]}
            for edge in set(edges)
            if edge[0] in hash_ids and edge[1] in hash_ids
        ],
    }
    graph_info = json.dumps(graph_info)

    with open(ZOLA_DIR / "static/js/graph_info.js", "w") as f:
        f.write(f"var graph_data={graph_info}")


def step4():
    """
    Parse markdown files contents
    """

    print_step("PARSING MARKDOWN FILES")
    md_files = list(DOCS_DIR.glob("**/*.md"))
    for md_file in md_files:
        content = [line.rstrip() for line in open(md_file, "r").readlines()]

        if str(md_file).endswith("_index.md"):
            continue

        content = remove_frontmatters(content)
        content = filter_lines(md_file, content)
        content = write_frontmatters(md_file, content)
        open(md_file, "w").write("\n".join(content))

    parse_graph()


if __name__ == "__main__":
    step1()
    step2()
    step3()
    step4()
