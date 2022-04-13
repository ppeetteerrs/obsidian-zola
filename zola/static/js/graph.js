// Query dark mode setting
function isDark() {
	return localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia("(prefers-color-scheme: dark)").matches);
}


// Get graph element
var container = document.getElementById("graph");

// Get nodes and edges from generated javascript
var nodes = new vis.DataSet(graph_data.nodes);
var edges = new vis.DataSet(graph_data.edges);
var max_node_val = Math.max(...nodes.map((node) => node.value));

// Get URL of current page and also current node
var curr_url = decodeURI(window.location.href.replace(location.origin, ""));
if (curr_url.endsWith("/")) {
	curr_url = curr_url.slice(0, -1)
}
var curr_node = nodes.get({
	filter: node => node.url == curr_url
});

// Highlight current node and set to center
if (curr_node.length > 0) {
	curr_node = curr_node[0];
	nodes.update({
		id: curr_node.id,
		value: Math.max(4, max_node_val * 2.5),
		shape: "star",
		color: "#a6a7ed",
		font: {
			strokeWidth: 1
		},
		x: 0,
		y: 0
	});
} else {
	curr_node = null;
}

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
	if (curr_node) {
		graph.focus(curr_node.id, {
			scale: graph.getScale() * 1.8
		});
	} else {
		var clientHeight = container.clientHeight;
		console.log(clientHeight);
		graph.moveTo({
			position: {
				x: 0,
				y: -clientHeight / 3
			},
			scale: graph.getScale() * 1.2
		});
	}
});