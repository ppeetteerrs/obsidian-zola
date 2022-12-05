import re
from typing import Dict, List, Tuple

from utils import (
    DocLink,
    DocPath,
    Settings,
    parse_graph,
    pp,
    raw_dir,
    site_dir,
    write_settings, convert_metadata_to_html, to_prerender_links,
)

if __name__ == "__main__":

    Settings.parse_env()
    Settings.sub_file(site_dir / "config.toml")
    Settings.sub_file(site_dir / "content/_index.md")
    Settings.sub_file(site_dir / "templates/macros/footer.html")
    Settings.sub_file(site_dir / "static/js/graph.js")

    nodes: Dict[str, str] = {}
    edges: List[Tuple[str, str]] = []
    section_count = 0

    all_paths = list(sorted(raw_dir.glob("**/*")))

    for path in [raw_dir, *all_paths]:
        doc_path = DocPath(path)
        if doc_path.is_file:
            if doc_path.is_md:
                # Page
                content = doc_path.content
                print(f'content {len(content)} for {doc_path.page_title}')
                if len(content) < 2:
                    print(f"Skipping {doc_path} because it is empty")
                    continue
                # meta_data = doc_path.metadata # maybe in the future we can extract metadata from inline yaml
                meta_data = doc_path.frontmatter
                if meta_data.get('graph', True):
                    nodes[doc_path.abs_url] = doc_path.page_title
                print(f"Found metadata for {doc_path.abs_url}: {meta_data}")
                parsed_lines: List[str] = []
                links = []
                for line in content:
                    parsed_line, linked = DocLink.parse(line, doc_path)
                    links += linked
                    # Fix LaTEX new lines
                    parsed_line = re.sub(r"\\\\\s*$", r"\\\\\\\\", parsed_line)

                    parsed_lines.append(parsed_line)

                    if meta_data.get('graph', True):
                        edges.extend([doc_path.edge(rel_path) for rel_path in linked])
                content = [
                    "---",
                    f'title: "{doc_path.page_title}"',
                    f"date: {doc_path.modified}",
                    f"updated: {doc_path.modified}",
                    "template: docs/page.html",
                    "extra:",
                    f"    prerender: {links}",
                    "---",
                    # To add last line-break
                    "",
                ]
                doc_path.write([
                    "\n".join(content),
                    convert_metadata_to_html(meta_data),
                    *parsed_lines])
                print(f"Found page: {doc_path.new_rel_path}")
            else:
                # Resource
                doc_path.copy()
                print(f"Found resource: {doc_path.new_rel_path}")
        else:
            """Section"""
            # Frontmatter
            # TODO: sort_by depends on settings
            content = [
                "---",
                f'title: "{doc_path.section_title}"',
                "template: docs/section.html",
                f"sort_by: {Settings.options['SORT_BY']}",
                f"weight: {section_count}",
                "extra:",
                f"    sidebar: {doc_path.section_sidebar}",
                "---",
                # To add last line-break
                "",
            ]
            section_count += 1
            doc_path.write_to("_index.md", "\n".join(content))
            print(f"Found section: {doc_path.new_rel_path}")

    pp(nodes)
    pp(edges)
    parse_graph(nodes, edges)
    write_settings()
