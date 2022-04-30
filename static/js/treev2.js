// Globals
const NODE_TYPES = {
  C: "C",
  U: "U",
  N: "N",
}

const NODE_DIM = {
  C: [250, 60],
  N: [150, 150],
  U: [150, 150],
}

const RATIO = 1.5 // transform gap between nodes

const skills1 = [
  {id: "user", label: "User", nodeType: "U" },
  {id: "languages", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "prgramming-fundamentals", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "markdown", label:"Languages", parentId: "user", nodeType: "C" },
  {
    parentId: "languages",
    id: "python",
    label: 'Python', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N"
  }, 
  {
    parentId: "python",
    id: "django",
    label: 'Django', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 3, 
    descrption: ["I'm alright at django"],
    nodeType: "N"
  },
  {
    parentId: "languages",
    id: "javascript",
    label: 'Javascript', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N"
  },
  {
    parentId: "javascript",
    id: "vue",
    label: 'Django', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 3, 
    descrption: ["I'm alright at django"],
    nodeType: "N"
  },
  {
    parentId: "javascript",
    id: "react",
    label: 'Django', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 3, 
    descrption: ["I'm alright at django"],
    nodeType: "N"
  },
  
]


// TODO: HTTP GET SKILLS

function getSkills() {
  return skills1
}
const skills = getSkills()

let id = 0

function getNodeToNodePathString(d) {
  console.log(d.source._id)
  return "M" + (d.source.x/RATIO + 75) + "," + d.source.y/1.5
    + " l" + (d.target.x - d.source.x)/1.5 + "," + (d.target.y - d.source.y)/1.5
}

function getCategoryToNodePathString(d) {
  let offset = 125
  // d.target.x = d.target.x + offset

  let targetX = d.target.x
  let sourceX = d.source.x
  let sourceY = d.source.y
  let targetY = d.target.y
  d.target._id = id
  id += 1

  

  return "M" + (sourceX/RATIO + offset) + "," + sourceY/RATIO
  + " l" + (targetX - sourceX)/RATIO + "," + (targetY - sourceY)/RATIO
}

const container = d3.select("#treeContainer")


const width = document.getElementById('treeContainer').clientWidth;
const height = document.getElementById('treeContainer').clientHeight;
const CNodeWidth = 250;


const treemap = d3.tree().size([height, width]);
let hierarchy = treemap(d3.stratify()(skills));

const svg = container.append("svg")
.attr("width", width)
.attr("height", height)
// .attr("viewBox", "0 0 2500 2500") // for zooming in/out

const tree = svg.append("g")

const links = tree
  .selectAll("g")
  .data(hierarchy.links())
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", d => {
    if (d.source.data.nodeType === NODE_TYPES.C) {
      return getCategoryToNodePathString(d)
    }
    return getNodeToNodePathString(d)
  })
  .style("stroke", "black")

const node = tree
  .selectAll("g")
  .data(hierarchy.descendants())
  .enter()
  .append("rect") //Potential problem line
  .attr("class", d => {
    switch (d.data.nodeType) {
      case NODE_TYPES.U:
        return 'node-user'
      case NODE_TYPES.C:
        return 'node-category'
      default:
        return 'node'
    }
  })
  .attr("width", d => {
    return NODE_DIM[d.data.nodeType][0]
  })
  .attr("height", d => NODE_DIM[d.data.nodeType][1])
  .attr("rx", d => d.data.nodeType === NODE_TYPES.U ? "75" : "15")
  .attr("ry", d => d.data.nodeType === NODE_TYPES.U ? "75" : "15")
  .attr("x", d => {
    return d.x /1.5
  })
  .attr("y", d => d.y /1.5)