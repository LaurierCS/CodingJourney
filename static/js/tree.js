// <script src="https://d3js.org/d3.v7.min.js"></script>

// Globals

/**
 * @constant
 * Different of node types.
 * C -> Category;
 * U -> User;
 * N -> Node;
 */
const NODE_TYPES = {
  C: "C",
  U: "U",
  N: "N",
};

/**
 * @constant
 * Node sizes on the tree.
 * Reflect the render size of a node.
 * Does not affect the nodeSize of a treemap.
 */
const NODE_DIM = {
  C: [250, 60],
  N: [150, 150],
  U: [150, 150],
};

/**
 * @constant
 */
const NODE_IMG_SIZE = 120

const width = document.getElementById("treeContainer").clientWidth;
const height = document.getElementById("treeContainer").clientHeight;
const viewBox = {
  x: -width / 2 - NODE_DIM.U[0] * 2,
  y: 0,
  width: width * 1.5, // zoom out view
  height: height * 1.5, // zoom out view
};

// FUNCTIONS

function getSkills() {
  if (tree_data.length < 1) return [];

  if (tree_data[0].fields === undefined) {
    for (let elem of tree_data) { 
      elem.parentId = elem.parentId_id
      elem.nodeType = elem.node_type
    }
    return tree_data
  }
 
  
  let returnList = []
  for (let elem of tree_data){ 
    let fields = elem.fields
    fields.id = elem.pk
    fields.nodeType = elem.fields.node_type
    // console.log(elem.fields)
    returnList.push(fields)
  }
    
  // console.log(returnList)
  return returnList;
}
const skills = getSkills();

function getLinkPath(d) {
  const halfNodeSize = 75;

  // We want the links from the User Node to start from the center of the node instead of the top.
  if (d.source.data.nodeType === NODE_TYPES.U) {
    return (
      "M" +
      (d.source.x + halfNodeSize) +
      "," +
      (d.source.y + halfNodeSize) +
      " l" +
      (d.target.x - d.source.x) +
      "," +
      (d.target.y - d.source.y - halfNodeSize)
    );
  }

  // handle all other links that are not connecting a User Node
  return (
    "M" +
    (d.source.x + halfNodeSize) +
    "," +
    d.source.y +
    " l" +
    (d.target.x - d.source.x) +
    "," +
    (d.target.y - d.source.y)
  );
}

function onNodeClick(e, d) {

  if (d.data.nodeType === NODE_TYPES.U || d.data.nodeType === NODE_TYPES.C) {
    return;
  }

  // check if sidebar exists or not
  if (!window.nodeSideBar) {
    window.nodeSideBar = new NodeSideBar("nsb")
  }

  nodeSideBar.show(d);
}

function getViewBoxString(x, y, w, h) {
  return `${x} ${y} ${w} ${h}`;
}

function getPoint(e) {
  let point = { x: -1, y: -1 };

  if (e.targetTouches) {
    point.x = e.targetTouches[0].clientX;
    point.y = e.targetTouches[0].clientY;
  } else {
    point.x = e.clientX;
    point.y = e.clientY;
  }

  return point;
}

function onPointerDown(e) {
  e.preventDefault()
  isPointerDown = true;
  let point = getPoint(e);
  originPoint.x = point.x;
  originPoint.y = point.y;
}

function onPointerUp(e) {
  e.preventDefault()
  isPointerDown = false;

  viewBox.x = newViewBox.x;
  viewBox.y = newViewBox.y;
}

function onPointerMove(e) {
  if (!isPointerDown) return;

  e.preventDefault();
  let cursorPossition = getPoint(e);

  newViewBox.x = viewBox.x - (cursorPossition.x - originPoint.x);
  newViewBox.y = viewBox.y - (cursorPossition.y - originPoint.y);

  let viewBoxString = getViewBoxString(
    newViewBox.x,
    newViewBox.y,
    viewBox.width,
    viewBox.height
  );
  svgEl.setAttribute("viewBox", viewBoxString);
}

function onZoom(e) {
  // do not let user zoom when panning.
  if (isPointerDown) return;

  // 1 for zoom in, -1 for zoom out
  let sign = Math.sign(e.deltaY);
  let zoomRatioWidth = viewBox.width * 0.1;
  let zoomRatioHeight = viewBox.height * 0.1;

  if (sign < 0) {
    // zoom out
    viewBox.width = viewBox.width - zoomRatioWidth;
    viewBox.height = viewBox.height - zoomRatioHeight;
  } else {
    viewBox.width = viewBox.width + zoomRatioWidth;
    viewBox.height = viewBox.height + zoomRatioHeight;
  }
  svgEl.setAttribute(
    "viewBox",
    getViewBoxString(viewBox.x, viewBox.y, viewBox.width, viewBox.height)
  );
}
// END OF FUNCTIONS

// START BUILDING TREE
const container = d3.select("#treeContainer");

const treemap = d3
  .tree()
  .size([height, width])
  .nodeSize([225, 300])
  .separation((a, b) => {
    // todo: determine the space between category nodes based on the lenght of the labels.
    if (
      a.parent === b.parent &&
      a.data.nodeType === NODE_TYPES.C &&
      b.data.nodeType === NODE_TYPES.C
    ) {
      return 2;
    }

    return 1;
  }); 
const hierarchy = treemap(d3.stratify()(skills));
const descendants = hierarchy.descendants()
 
const svg = container
  .append("svg")
  .attr("id", "#tree")
  .attr("width", width)
  .attr("height", height)
  .attr("style", "cursor: move;")
  .attr("viewBox", getViewBoxString(viewBox.x, viewBox.y, viewBox.width, viewBox.height)); // for zooming in/out

// adding a clip path definition to make the circular view of the user node
// so a bigger and squared image would fill the circular area and hide the overflow
const defs = svg.append("defs");
defs
  .append("clipPath")
  .attr("id", "user-clip")
  .append("rect")
  .attr("width", NODE_DIM.U[0])
  .attr("height", NODE_DIM.U[1])
  .attr("rx", NODE_DIM.U[0]/2)
  .attr("ry", NODE_DIM.U[0]/2)

const tree = svg.append("g").attr("data-tree", "true");

// links are separated from the node group
// it is easier to draw the links this way
const links = tree
  .selectAll(".link") 
  .data(hierarchy.links())
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", (d) => getLinkPath(d))

/**
 * Put all nodes into separate groups to handle on hover effects.
 * bug: fixed size category nodes will become a problem if the category name is too long.
 * bug: the text will overflow, the node wont expand.
 * todo: adjust category node size dynamically.
 */
const nodes = tree
  .selectAll(".node")
  .data(descendants)
  .enter()
  .append("g")
  .attr("class", "node-group")
  .on("click", onNodeClick);

const rects = nodes
  .append("rect")
  .attr("class", (d) =>
  d.data.nodeType === NODE_TYPES.C ? "node-category" : d.data.nodeType === NODE_TYPES.U ? "node node-user" : "node"
  )
  .attr("width", (d) => NODE_DIM[d.data.nodeType][0])
  .attr("height", (d) => NODE_DIM[d.data.nodeType][1])
  .attr("rx", (d) => (d.data.nodeType === NODE_TYPES.U ? NODE_DIM.U[0]/2 : 15))
  .attr("ry", (d) => (d.data.nodeType === NODE_TYPES.U ? NODE_DIM.U[0]/2 : 15))
  .attr("x", (d) => d.data.nodeType === NODE_TYPES.C ? d.x - 50 : d.x )
  .attr("y", (d) => d.y)
  .attr("data-node-id", d => d.id)

const nodeLabel = nodes
  .append("text")
  .text(d => {
    if (d.data.nodeType === NODE_TYPES.U && window.username) {
      return window.username;
    }

    return d.data.name;
  })
  .attr("class", d => d.data.nodeType !== NODE_TYPES.C ? "node-label" : "node-label node-title")
  .attr("x", d => {
    // because the x in d.x does not reflect the x position of the rectangle
    // to center the text for a category node, we need to get the x from the rect element directly.
    let x;
    if (d.data.nodeType === NODE_TYPES.C) {
      let r = document.querySelector(`rect[data-node-id="${d.id}"`)
      x = parseFloat(r.getAttribute("x"))
    } else {
      x = d.x
    }
    return x + NODE_DIM[d.data.nodeType][0] / 2;
  })
  .attr("y", d => d.data.nodeType === NODE_TYPES.C ? d.y + NODE_DIM.C[1] / 2 : d.y + NODE_DIM[d.data.nodeType][1] + 20)
  .attr("text-anchor", "middle")
  .attr("dominant-baseline", "middle")
  .attr("data-node-label-id", d => d.id)

const nodeImage = nodes
  .append("image")
  .attr("href", d => {
    // todo: return iconHref instead

    if (d.data.nodeType === NODE_TYPES.U && window.profile_pic) {
      return window.profile_pic;
    }

    return "/static/images/svg/badge.svg" // todo: change to return actual icon when available
  })
  .attr("class", "node-image")
  .attr("width", d => d.data.nodeType !== NODE_TYPES.C ? d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : NODE_DIM.U[0] : 0)
  .attr("height", d => d.data.nodeType !== NODE_TYPES.C ? d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : NODE_DIM.U[1] : 0)
  .attr("x", d => d.x + NODE_DIM[d.data.nodeType][0] / 2 - (d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : NODE_DIM.U[0]) / 2)
  .attr("y", d => d.y + NODE_DIM[d.data.nodeType][1] / 2 - (d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : NODE_DIM.U[1]) / 2)
  .attr("clip-path", d => d.data.nodeType === NODE_TYPES.U ? "url(#user-clip)" : "")
  .attr("preserveAspectRatio", "none")
  .attr("data-node-image-id", d => d.id)

// add panning
const originPoint = { x: -1, y: -1 };
const newViewBox = { ...viewBox };
const svgEl = document.getElementById("#tree");
let isPointerDown = false; 

if (window.PointerEvent) {
  svgEl.addEventListener("pointerdown", onPointerDown);
  svgEl.addEventListener("pointerup", onPointerUp);
  svgEl.addEventListener("pointerleave", onPointerUp);
  svgEl.addEventListener("pointermove", onPointerMove);
} else {
  // Add all mouse events listeners fallback
  svgEl.addEventListener("mousedown", onPointerDown);
  svgEl.addEventListener("mouseup", onPointerUp);
  svgEl.addEventListener("mouseleave", onPointerUp);
  svgEl.addEventListener("mousemove", onPointerMove);

  // Add all touch events listeners fallback
  svgEl.addEventListener("touchstart", onPointerDown);
  svgEl.addEventListener("touchend", onPointerUp);
  svgEl.addEventListener("touchmove", onPointerMove);
}

// add zoom in/out
svgEl.addEventListener("wheel", onZoom);
