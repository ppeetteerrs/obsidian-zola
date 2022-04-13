import json
import math
import os
import re
import site
from datetime import datetime
from distutils.util import strtobool
from os import environ
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union
from urllib import parse as urlparse

from numpy import isin
from slugify import slugify

# ---------------------------------------------------------------------------- #
#                                 General Utils                                #
# ---------------------------------------------------------------------------- #


def print_step(msg: str):
    print(msg.center(100, "-"))


def slugify_path(path: Union[str, Path]) -> str:
    path = Path(path)
    os_path = "/".join(slugify(item) for item in str(path.parent).split("/"))
    name = ".".join(slugify(item) for item in path.stem.split("."))
    suffix = slugify(path.suffix)

    if name == "":
        return os_path
    elif suffix == "":
        return f"{os_path}/{name}"
    else:
        return f"{os_path}/{name}.{suffix}"


# ---------------------------------------------------------------------------- #
#                            File Content Processing                           #
# ---------------------------------------------------------------------------- #


def process_lines(path: Path, fn: Callable[[str], str]):
    """
    Applies a function to the rstrip-ed lines of a file and write them back.
    """

    content = "\n".join([fn(line.rstrip()) for line in open(path, "r").readlines()])
    open(path, "w").write(content)


# ---------------------------------------------------------------------------- #
#                                  Regex Magic                                 #
# ---------------------------------------------------------------------------- #


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
        (combined, title, url)
        for combined, title, url in re.findall(
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
        (combined, title, url, heading)
        for combined, title, url, heading in re.findall(
            r"(\[(.+?)\]\((?!http)(\S+?)(?:\.md)?(#\S+)?\))", line
        )
        if not no_inner_link(combined)
    ]


# ---------------------------------------------------------------------------- #
#                                   Settings                                   #
# ---------------------------------------------------------------------------- #


class Settings:
    """
    Changes to mutable class variable fields are broadcasted across all instances no matter where the change happens. The class object and all instances would receive the change no matter the setting method:
    - assign to Settings.default["xxx]
    - change cls.default["xxx"] inside class method
    - assign to instance.default["xxx"]
    - change self.default["xxx"] inside instance method
    """

    options: Dict[str, Optional[str]] = {
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
        "SLUGIFY": "n",
        "HOME_GRAPH": "n",
        "PAGE_GRAPH": "n",
    }
    site_dir: Path = Path(__file__).resolve().parent / "build"
    draft_dir: Path = site_dir / "__docs"
    docs_dir: Path = site_dir / "content/docs"

    @classmethod
    def is_true(cls, key: str) -> bool:
        val = cls.options[key]
        return bool(strtobool(val)) if val else False

    @classmethod
    @property
    def sections(cls) -> List[Path]:
        """
        Get the paths to different sections in the draft directory.
        """

        return list(sorted(cls.draft_dir.glob("**/**"), key=lambda x: str(x).lower()))

    @classmethod
    @property
    def pages(cls) -> List[Path]:
        """
        Get the paths to different pages in the draft directory.
        """

        return list(cls.draft_dir.glob("**/*.md"))

    # @classmethod
    # def read_file(cls, path: Path) -> List[str]:
    #     """
    #     Reads the content from a file.
    #     """

    #     with open(path, "r") as f:
    #         return [line.rstrip() for line in f.readlines()]

    @classmethod
    def write_doc(cls, path: str, content: Union[str, List[str]]):
        """
        Write content to a file in the docs directory.
        """

        # Make parent directories
        file_path = cls.docs_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        with open(file_path, "w") as f:
            if isinstance(content, str):
                f.write(content)
            else:
                f.write("\n".join(content))

    @classmethod
    def parse_env(cls):
        """
        Checks the env variables for required settings. Also stores the set variables.
        """

        for key in cls.options.keys():
            required = cls.options[key] is None

            if key in environ:
                cls.options[key] = environ[key]
            else:
                if required:
                    raise Exception(f"FATAL ERROR: build.environment.{key} not set!")
        print(cls.options)

    @classmethod
    def sub_line(cls, line: str) -> str:
        """
        Substitutes variable placeholders in a line.
        """

        for key, val in cls.options.items():
            line = line.replace(f"___{key}___", val if val else "")
        return line

    @classmethod
    def sub_file(cls, path: Path):
        """
        Substitutes variable placeholders in a file.
        """

        process_lines(path, cls.sub_line)


# ---------------------------------------------------------------------------- #
#                               Parsing Sections                               #
# ---------------------------------------------------------------------------- #
def section_info(path: Path, to_slug: bool) -> Tuple[str, str]:
    """
    Returns the title and (slugified, if to_slug) path of the section.
    """

    # Parse section title.
    title = re.sub(r"^.*?__docs/*", "", str(path))

    # Parse path to section folder
    if to_slug:
        slug_path = slugify_path(title)
    else:
        slug_path = title

    # Root section is called "MAIN". Placed here to avoid messing up slugified path.
    if title == "":
        title = "main"
    else:
        slug_path += "/"
    return title, slug_path


# ---------------------------------------------------------------------------- #
#                                 Parsing Pages                                #
# ---------------------------------------------------------------------------- #


def page_info(path: Path, to_slug: bool) -> Tuple[str, Path]:
    """
    Returns the (slugified) path to the page and its parent.
    """

    # Relative path of current file
    # path: <site_dir>/content/xxx/yyy.md
    # abs_path: xxx/yyy (slugified if needed)
    abs_path = re.sub(r"^.*?__docs/*", "/docs/", str(path)).replace(".md", "")
    if to_slug:
        abs_path = slugify_path(abs_path)
    return abs_path, Path(abs_path).parent


def parse_page_line(
    line: str, page_path: str, page_parent: Path, to_slug: bool
) -> Tuple[str, List[Tuple[str, str]]]:

    # Parse internal markdown references (knowledge graph edges)
    edges: List[Tuple[str, str]] = []
    for _, _, url in get_md_links(line):
        # Turn markdown URL to a normalized (slugified) path
        url_path = urlparse.unquote(str((page_parent / url).resolve()))
        if to_slug:
            url_path = slugify_path(url_path)
        edges.append(tuple(sorted([page_path, url_path])))

    # Parse the line
    parsed_line = line

    # Turn any relative links into (slugified) absolute links
    for combined, title, url, heading in get_internal_links(line):
        # Unquote, add parent dir, slugify if needed, quote
        abs_url = str((page_parent / urlparse.unquote(url)).resolve())
        if to_slug:
            abs_url = slugify_path(abs_url)
        abs_url = urlparse.quote(abs_url)

        parsed_line = parsed_line.replace(combined, f"[{title}]({abs_url}{heading})")

    # Replace ending double forward slashes (in LaTEX) to fix line breaks
    parsed_line = re.sub(r"\\\\\s*$", r"\\\\\\\\", parsed_line)

    return parsed_line, edges


def parse_page(
    path: Path, to_slug: bool
) -> Tuple[List[str], str, str, List[Tuple[str, str]]]:
    """
    Returns page content, page title, page (slugified path), page edges
    """

    # Parse path information
    page_path, page_parent = page_info(path, to_slug)

    # Parse each line and also get knowledge graph edges
    edges: List[Tuple[str, str]] = []
    parsed_lines: List[str] = []

    for line in open(path, "r").readlines():
        parsed_line, edges = parse_page_line(line, page_path, page_parent, to_slug)
        parsed_lines.append(parsed_line)
        edges.extend(edges)

    # Write frontmatters

    # Use Titlecase file name (preserving uppercase words) as title
    page_title = " ".join(
        [item if item[0].isupper() else item.title() for item in path.stem.split(" ")]
    )
    # Use last modified time as creation and updated time
    modified = datetime.fromtimestamp(os.path.getmtime(path))
    content = [
        "---",
        f"title: {page_title}",
        f"date: {modified}",
        f"updated: {modified}",
        "template: docs/page.html",
        "---",
        *parsed_lines,
    ]

    return content, page_title, page_path, edges


# ---------------------------------------------------------------------------- #
#                                Knowledge Graph                               #
# ---------------------------------------------------------------------------- #

PASTEL_COLORS = [
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
