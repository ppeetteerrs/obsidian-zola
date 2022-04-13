import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

from utils import PASTEL_COLORS, Settings, parse_page, print_step, section_info


def parse_section(idx: int, path: Path):
    # Parse section title.
    title, slug_path = section_info(path, Settings.is_true("SLUGIFY"))

    # Frontmatter
    fm = [
        "---",
        f"title: {title}",
        "template: docs/section.html",
        f"sort_by: {Settings.options['SORT_BY']}",
        f"weight: {idx}",
        "---",
    ]

    Settings.write_doc(f"{slug_path}_index.md", fm)
    print(f"Found section: {slug_path}")


def parse_pages() -> Tuple[Dict[str, str], List[Tuple[str, str]]]:
    """
    Parse all pages and return nodes and edges of knowledge graph
    """

    # key: relative path, value: title
    nodes: Dict[str, str] = {}
    # from relative path, to relative path
    edges: List[Tuple[str, str]] = []

    for path in Settings.pages:
        content, page_title, page_path, edges = parse_page(
            path, Settings.is_true("SLUGIFY")
        )
        Settings.write_doc(f"../{page_path}.md", content)
        print(f"Found page: {page_path}")

        nodes[page_path] = page_title
        edges.extend(edges)
    return nodes, edges


def parse_graph(nodes: Dict[str, str], edges: List[Tuple[str, str]]):

    # Assign increasing ID value to each node
    node_ids = {k: i for i, k in enumerate(nodes.keys())}

    # Filter out edges that does not connect two known nodes (i.e. ghost pages)
    existing_edges = [
        edge for edge in set(edges) if edge[0] in node_ids and edge[1] in node_ids
    ]

    # Count the number of edges connected to each node
    edge_counts = {k: 0 for k in nodes.keys()}
    for i, j in existing_edges:
        edge_counts[i] += 1
        edge_counts[j] += 1

    # Choose the most connected nodes to be colored
    top_nodes = {
        node_url: i
        for i, (node_url, _) in enumerate(
            list(sorted(edge_counts.items(), key=lambda k: -k[1]))[: len(PASTEL_COLORS)]
        )
    }

    # Generate graph data
    graph_info = {
        "nodes": [
            {
                "id": node_ids[url],
                "label": title,
                "url": url,
                "color": PASTEL_COLORS[top_nodes[url]] if url in top_nodes else None,
                "value": math.log10(edge_counts[url] + 1) + 1,
                "opacity": 0.1,
            }
            for url, title in nodes.items()
        ],
        "edges": [
            {"from": node_ids[edge[0]], "to": node_ids[edge[1]]}
            for edge in set(edges)
            if edge[0] in node_ids and edge[1] in node_ids
        ],
    }
    graph_info = json.dumps(graph_info)

    with open(Settings.site_dir / "static/js/graph_info.js", "w") as f:
        f.write(f"var graph_data={graph_info}")


if __name__ == "__main__":
    print_step("LOADING ENVIRONMENT VARIABLES")
    Settings.parse_env()

    print_step("FILE SUBSTITUTIONS")
    Settings.sub_file(Settings.site_dir / "config.toml")
    Settings.sub_file(Settings.site_dir / "content/_index.md")

    print_step("PARSING SECTIONS")
    for idx, path in enumerate(Settings.sections):
        print(path)
        parse_section(idx, path)

    print_step("PARSING PAGES")
    nodes, edges = parse_pages()

    print_step("PARSING GRAPH")
    parse_graph(nodes, edges)
