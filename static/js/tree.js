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

const width = document.getElementById("treeContainer").clientWidth;
const height = document.getElementById("treeContainer").clientHeight;
const viewBox = {
  x: -width / 2,
  y: 0,
  width,
  height,
};

const skills1 = [
  { id: "user", label: "User", nodeType: "U" },
  { id: "languages", label: "Languages", parentId: "user", nodeType: "C" },
  { id: "a", label: "Languages", parentId: "user", nodeType: "C" },
  { id: "b", label: "Languages", parentId: "user", nodeType: "C" },
  { id: "c", label: "Languages", parentId: "user", nodeType: "C" },
  { id: "d", label: "Languages", parentId: "user", nodeType: "C" },
  { id: "e", label: "Languages", parentId: "user", nodeType: "C" },
  {
    parentId: "languages",
    id: "python",
    label: "Python",
    iconHref: "static/images/python_logo.png",
    skillLevel: 4.5,
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N",
  },
  {
    parentId: "python",
    id: "django",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "languages",
    id: "javascript",
    label: "Javascript",
    iconHref: "static/images/python_logo.png",
    skillLevel: 4.5,
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N",
  },
  {
    parentId: "javascript",
    id: "vue",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "javascript",
    id: "react",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "a",
    id: "aa",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "a",
    id: "aaa",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "a",
    id: "aaaa",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "a",
    id: "aaaaa",
    label: "Django",
    iconHref: "static/images/python_logo.png",
    skillLevel: 3,
    descrption: ["I'm alright at django"],
    nodeType: "N",
  },
  {
    parentId: "b",
    id: "bb",
    label: "Javascript",
    iconHref: "static/images/python_logo.png",
    skillLevel: 4.5,
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N",
  },
  {
    parentId: "bb",
    id: "bbb",
    label: "Javascript",
    iconHref: "static/images/python_logo.png",
    skillLevel: 4.5,
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N",
  },
  {
    parentId: "bb",
    id: "bbbb",
    label: "Javascript",
    iconHref: "static/images/python_logo.png",
    skillLevel: 4.5,
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N",
  },
];

function getSkills() {
  // TODO: HTTP GET SKILLS
  return skills1;
}
const skills = getSkills();

function getLinkPath(d) {
  const halfNodeSize = 75;

  // We want the links from the User Node to start from the center of the node instead of the top.
  if (d.source.data.nodeType === NODE_TYPES.U) {
    return (
      "M" +
      (d.source.x  + halfNodeSize) +
      "," +
      (d.source.y + halfNodeSize)  +
      " l" +
      (d.target.x - d.source.x)  +
      "," +
      (d.target.y - d.source.y - halfNodeSize) 
    );
  }

  // handle all other links that are not connecting a User Node
  return (
    "M" +
    (d.source.x  + halfNodeSize) +
    "," +
    d.source.y  +
    " l" +
    (d.target.x - d.source.x)  +
    "," +
    (d.target.y - d.source.y) 
  );
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
let hierarchy = treemap(d3.stratify()(skills));

const svg = container
  .append("svg")
  .attr("id", "#tree")
  .attr("width", width)
  .attr("height", height)
  .attr("style", "cursor: move;")
  .attr("viewBox", (d) => getViewBoxString(viewBox.x, viewBox.y, viewBox.width, viewBox.height)); // for zooming in/out

const tree = svg.append("g");

const links = tree
  .selectAll(".link")
  .data(hierarchy.links())
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", (d) => getLinkPath(d));

const node = tree
  .selectAll(".node")
  .data(hierarchy.descendants())
  .enter()
  .append("rect") //Potential problem line
  .attr("class", (d) =>
    d.data.nodeType === NODE_TYPES.C ? "node-category" : "node"
  )
  .attr("width", (d) => NODE_DIM[d.data.nodeType][0])
  .attr("height", (d) => NODE_DIM[d.data.nodeType][1])
  .attr("rx", (d) => (d.data.nodeType === NODE_TYPES.U ? "75" : "15"))
  .attr("ry", (d) => (d.data.nodeType === NODE_TYPES.U ? "75" : "15"))
  .attr("x", (d) => {
    switch (d.data.nodeType) {
      case NODE_TYPES.C:
        // handle cat node
        return d.x - 50;
      default:
        return d.x;
    }
  })
  .attr("y", (d) => d.y);

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
  isPointerDown = true;
  let point = getPoint(e);
  originPoint.x = point.x;
  originPoint.y = point.y;
}

function onPointerUp() {
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
