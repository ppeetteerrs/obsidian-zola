import os
import re
from datetime import datetime
from os import environ
from pathlib import Path
from typing import Callable, List

ENV_VARS = [
    "SITE_URL",
    "SITE_TITLE",
    "TIMEZONE",
    "REPO_URL",
    "LANDING_PAGE",
    "LANDING_TITLE",
    "LANDING_DESCRIPTION",
    "LANDING_BUTTON",
]

ZOLA_DIR = Path(__file__).resolve().parent
DOCS_DIR = ZOLA_DIR / "content" / "docs"


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
    for item in ENV_VARS:
        if item not in environ:
            print(f"WARNING: build.environment.{item} not set!")
            environ[item] = f"build.environment.{item}"
        else:
            print(f"{item}: {environ[item]}")


def step2():
    """
    Substitute netlify.toml settings into config.toml and landing page
    """

    print_step("SUBSTITUTING CONFIG FILE AND LANDING PAGE")

    def sub(line: str) -> str:
        for env_var in ENV_VARS:
            line = line.replace(f"___{env_var}___", environ[env_var])
        return line

    process_lines(ZOLA_DIR / "config.toml", sub)
    process_lines(ZOLA_DIR / "content" / "_index.md", sub)


def step3():
    """
    Generate _index.md for each section
    """

    print_step("GENERATING _index.md")
    sections = list(DOCS_DIR.glob("**/**"))
    content = None
    for section in sections:
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


def filter_lines(file: Path, content: List[str]) -> List[str]:
    """
    1. Replace obsidian relative links to valid absolute links
    2. Double escape latex newline
    """
    # Replace relative links
    parent_dir = f"{file.parents[0]}".replace(str(ZOLA_DIR / "content"), "").replace(
        " ", "%20"
    )

    # Markdown links: [xxx](yyy)
    # (\[.+?\]): Capture [xxx] part
    # \((?!http)(.+?)(?:.md)?\): Capture (yyy) part, ensuring that link is not http and remove .md from markdown files
    # (#.+)?: Capture any heading tags after ".md"
    replaced_links = [
        re.sub(
            r"(\[.+?\])\((?!http)(.+?)(?:.md)?(#.+)?\)",
            r"\1(" + parent_dir + r"/\2\3)",
            line,
        )
        for line in content
    ]

    # Replace ending double forward slashes (in LaTEX) to fix line breaks
    replaced_slashes = [
        re.sub(r"\\\\\s*$", r"\\\\\\\\", line) for line in replaced_links
    ]

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


if __name__ == "__main__":
    step1()
    step2()
    step3()
    step4()
