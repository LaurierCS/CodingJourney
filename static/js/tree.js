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

function getSkills() {
  let returnList = []
  // console.log(tree_data)
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

function onNodeClick(d) {
  // todo: implement on click behaviour
  console.log("Node click behaviour not implemented.");
}

const container = d3.select("#treeContainer");

const treemap = d3
  .tree()
  .size([height, width])
  .nodeSize([225, 300])
  .separation((a, b) => {
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
 * todo: adjust category node size dynamically.
 */
const nodes = tree
  .selectAll(".node")
  .data(descendants)
  .enter()
  .append("g")
  .attr("class", "node-group")

const rects = nodes
  .append("rect")
  .attr("class", (d) =>
  d.data.nodeType === NODE_TYPES.C ? "node-category" : "node"
  )
  .attr("width", (d) => NODE_DIM[d.data.nodeType][0])
  .attr("height", (d) => NODE_DIM[d.data.nodeType][1])
  .attr("rx", (d) => (d.data.nodeType === NODE_TYPES.U ? "75" : "15"))
  .attr("ry", (d) => (d.data.nodeType === NODE_TYPES.U ? "75" : "15"))
  .attr("x", (d) => d.data.nodeType === NODE_TYPES.C ? d.x - 50 : d.x )
  .attr("y", (d) => d.y)
  .attr("data-node-id", d => d.id)
  .on("click", onNodeClick);

const nodeLabel = nodes
  .append("text")
  .text(d => d.data.name)
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
    return "/static/images/python_logo.png"
  })
  .attr("class", "node-image")
  .attr("width", d => d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : 0) // todo: return actual size for user nodes
  .attr("height", d => d.data.nodeType === NODE_TYPES.N ? NODE_IMG_SIZE : 0) // todo: return actual szie for user nodes
  .attr("x", d => d.x + NODE_DIM[d.data.nodeType][0] / 2 - NODE_IMG_SIZE / 2)
  .attr("y", d => d.y + NODE_DIM[d.data.nodeType][1] / 2 - NODE_IMG_SIZE / 2)
  .attr("data-node-image-id", d => d.id)

// update viewbox
console.log(document.querySelector('g[data-tree="true"]').getClientRects())

// add panning
const originPoint = { x: -1, y: -1 };
const newViewBox = { ...viewBox };
const svgEl = document.getElementById("#tree");
let isPointerDown = false; 

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

svgEl.addEventListener("wheel", onZoom);
