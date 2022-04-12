// Query dark mode setting
function isDark() {
	return localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia("(prefers-color-scheme: dark)").matches);
}

// Get URL of current page
var curr_url = decodeURI(window.location.href.replace(location.origin, ""));
if (curr_url.endsWith("/")) {
	curr_url = curr_url.slice(0, -1)
}

// Get graph element
var container = document.getElementById("graph");

// Get nodes and edges from generated javascript
var nodes = new vis.DataSet(graph_data.nodes);
var edges = new vis.DataSet(graph_data.edges);

// Construct graph
var options = {
	nodes: {
		shape: "dot",
		color: isDark() ? "#8c8e91" : "#dee2e6",
		font: {
			face: "Inter",
			color: isDark() ? "#c9cdd1" : "#616469",
			strokeColor: isDark() ? "#c9cdd1" : "#616469",
		},
		scaling: {
			label: {
				enabled: true
			}
		},
	},
	edges: {
		color: { inherit: "both" },
		width: 0.8,
		smooth: {
			type: "continuous",
		},
		hoverWidth: 4,
	},
	interaction: {
		hover: true,
	},
	height: "100%",
	width: "100%",
	physics: {
		solver: "repulsion"
	}
};

var graph = new vis.Network(container, {
	nodes: nodes,
	edges: edges
}, options);

// Clickable URL
graph.on("selectNode", function (params) {
	if (params.nodes.length === 1) {
		var node = nodes.get(params.nodes[0]);
		window.open(node.url, "_blank");
	}
});

// Focus on current node + scaling
graph.once("afterDrawing", function () {
	var curr_node = nodes.get({
		filter: node => node.url == curr_url
	});
	console.log(curr_url);
	if (curr_node.length > 0) {
		var idx = curr_node[0].id;
		graph.focus(idx, {
			scale: graph.getScale() * 1.8
		});
		nodes.update({
			id: idx,
			value: 3,
			color: "#6667AB",
			borderWidth: 3,
			font: {
				strokeWidth: 1
			}
		});
	} else {
		graph.moveTo({
			scale: graph.getScale() * 1.8
		});
	}
});