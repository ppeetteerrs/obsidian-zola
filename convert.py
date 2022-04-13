import re
from typing import Dict, List, Tuple

from utils import DocLink, DocPath, Settings, parse_graph, pp, raw_dir, site_dir

if __name__ == "__main__":

    Settings.parse_env()
    Settings.sub_file(site_dir / "config.toml")
    Settings.sub_file(site_dir / "content/_index.md")

    nodes: Dict[str, str] = {}
    edges: List[Tuple[str, str]] = []
    section_count = 0

    all_paths = list(sorted(raw_dir.glob("**/*")))

    for path in [raw_dir, *all_paths]:
        doc_path = DocPath(path, False)
        if doc_path.is_file:
            if doc_path.is_md:
                # Page
                nodes[doc_path.md_path] = doc_path.page_title
                content = doc_path.content
                parsed_lines: List[str] = []
                for line in content:
                    parsed_line, linked = DocLink.parse(line, doc_path)
                    parsed_lines.append(re.sub(r"\\\\\s*$", r"\\\\\\\\", parsed_line))
                    edges.extend([doc_path.edge(rel_path) for rel_path in linked])

                content = [
                    "---",
                    f"title: {doc_path.page_title}",
                    f"date: {doc_path.modified}",
                    f"updated: {doc_path.modified}",
                    "template: docs/page.html",
                    "---",
                    *parsed_lines,
                ]
                doc_path.write(content)
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
                f"title: {doc_path.section_title}",
                "template: docs/section.html",
                f"sort_by: {Settings.options['SORT_BY']}",
                f"weight: {section_count}",
                "---",
            ]
            section_count += 1
            doc_path.write_to("_index.md", content)
            print(f"Found section: {doc_path.new_rel_path}")
    # pp(nodes)
    # pp(edges)
    parse_graph(nodes, edges)
