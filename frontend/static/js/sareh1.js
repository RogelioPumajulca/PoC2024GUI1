var viz;

function draw() {
    var config = {
        containerId: "viz",
        neo4j: {
            serverUrl: "neo4j://localhost:7687",
            serverUser: "neo4j",
            serverPassword: "neo4j",
        },
        visConfig: {
            edges: {
                color: "#000000",
                arrows: {
                    to: {enabled: true}
                }
            }
        },
        layout: {
            enabled: true,
            sortMethod: 'directed',
        },
        [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
        },
        labels: {
            "VERTEX": {
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                        function: {
                            label: vertexLabel,
                            title: NeoVis.objectToTitleHtml,
                            color: vertexColor
                        }
                    }
            }
        },
        relationships: {
            "EDGE": {
                label: "operation",
                color: "#ffffff",
                [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                    function: {
                        title: NeoVis.objectToTitleHtml
                    }
                }
            }
        },
        arrows: true,
        initialCypher: "MATCH (n:VERTEX)-[e:EDGE]->(p:VERTEX) WHERE (n.type = 'Process') SET n:POI WITH n,e,p MATCH (n:VERTEX)-[e:EDGE]->(p:VERTEX) RETURN n,e,p LIMIT 50;"
    };

    viz = new NeoVis.default(config);
    viz.render();
}


function truncate(string, n) {
    if (string.length <= n) {
        return string;
    }
    var subString = "";
    firstIndex = string.indexOf("/", 1);
    lastIndex = string.lastIndexOf("/");
    if (firstIndex != -1) {
        if (firstIndex != lastIndex) {
            subString = string.slice(0, firstIndex + 1) + "(...)" + string.slice(lastIndex);
        } else {
            subString = string.slice(0, firstIndex + 1) + "(...)" + string.slice(string.length - Math.floor(n/2) - 2);
        }
    } else {
        subString = string.slice(0, Math.floor(n/2)) + "(...)" + string.slice(string.length - Math.floor(n/2) - 2);
    }
    return subString;
}

function vertexLabel(node) {
    var label;
    switch (node.properties.type) {
        case "Process":
            label = node.properties.name;
            break;
        case "Artifact":
            switch (node.properties.subtype) {
                case "network socket":
                    label = node.properties["remote address"];
                    break;
                case "file":
                    label = node.properties.path;
                    break;
                case "directory":
                    label = node.properties.path;
                    break;
                case "unnamed pipe": 
                    label = node.properties["read fd"] + "-->" + node.properties["write fd"];
                    break;
                case "character device":
                    label = node.properties.path;
                    break;
            }
        break;
    }
    if (label == undefined) {
        label = node.properties.type;
    }
    return truncate(label, 15);
}


function vertexColor(node) {
    // switch (node.properties.type) {
    //     case "Process": return "#850808";
    //     case "Artifact":
    //         switch (node.properties.subtype) {
    //             case "network socket": return "#deba07";
    //             case "file": return "#3d7d05";
    //             case "directory": return "#204203";
    //             case "unnamed pipe": return "#4a4a4a";
    //             case "character device": return "#4a4a4a";
    //         }
    // }
    console.log(node.labels)
    if (node.labels.includes("POI")) {
        return "#850808";
    }
    return "#4a4a4a";
}