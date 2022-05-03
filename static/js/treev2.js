// Globals
const NODE_TYPES = {
  C: "C",
  U: "U",
  N: "N",
}

const NODE_DIM = {
  C: [50, 30],
  N: [150, 150],
  U: [150, 150],
}

const RATIO = 1 // transform gap between nodes

const skills1 = [
  {id: "user", label: "User", nodeType: "U" },
  {id: "languages", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "a", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "b", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "c", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "d", label:"Languages", parentId: "user", nodeType: "C" },
  {id: "e", label:"Languages", parentId: "user", nodeType: "C" },
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
  {
    parentId: "a",
    id: "aa",
    label: 'Django', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 3, 
    descrption: ["I'm alright at django"],
    nodeType: "N"
  },
  {
    parentId: "b",
    id: "bb",
    label: 'Javascript', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N"
  },
  {
    parentId: "bb",
    id: "bbb",
    label: 'Javascript', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"],
    nodeType: "N"
  },
  {
    parentId: "bb",
    id: "bbbb",
    label: 'Javascript', 
    iconHref: 'static/images/python_logo.png', 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"],
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
  return "M" + (d.source.x/RATIO + 75) + "," + d.source.y/RATIO
    + " l" + (d.target.x - d.source.x)/RATIO + "," + (d.target.y - d.source.y)/RATIO
}

// BUG: Placing is not working properly with the narrower version of a node
// function getCategoryToNodePathString(d) {
//   let offset = 125
//   d.target.x = d.target.x + offset

//   let targetX = d.target.x
//   let sourceX = d.source.x
//   let sourceY = d.source.y
//   let targetY = d.target.y
//   d.target._id = id
//   id += 1

//   return "M" + (sourceX/RATIO + offset) + "," + sourceY/RATIO
//   + " l" + (targetX - sourceX)/RATIO + "," + (targetY - sourceY)/RATIO
// }

const container = d3.select("#treeContainer")


const width = document.getElementById('treeContainer').clientWidth;
const height = document.getElementById('treeContainer').clientHeight;
const CNodeWidth = 250;


const treemap = d3.tree().size([height, width])
  .nodeSize([225, 300])
  .separation((a, b) => {
    
    // let width_a = NODE_DIM[a.data.nodeType][0]
    // let width_b = NODE_DIM[b.data.nodeType][0]
    // let width = width_a + width_b

    // let distance = width/2
    // console.log("distance", distance)

    // if (a.data.id === "react") a.y += 100

    return 2
  })
let hierarchy = treemap(d3.stratify()(skills));

const svg = container.append("svg")
.attr("width", width)
.attr("height", height)
.attr("viewBox", d => {
  return `0 0 ${width} ${height}`
}) // for zooming in/out

const tree = svg.append("g")
  .attr("transform", "translate(500, 0)")

const links = tree
  .selectAll(".link")
  .data(hierarchy.links())
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", d => getNodeToNodePathString(d))
  .style("stroke", "black")

const node = tree
  .selectAll(".node")
  .data(hierarchy.descendants())
  .enter()
  .append("rect") //Potential problem line
  .attr("class", d => d.data.nodeType === NODE_TYPES.C ? "node-category" : "node")
  .attr("width", '150')
  .attr("height", '150')
  .attr("rx", d => d.data.nodeType === NODE_TYPES.U ? "75" : "15")
  .attr("ry", d => d.data.nodeType === NODE_TYPES.U ? "75" : "15")
  .attr("x", d => {
    switch (d.data.nodeType) {
      case NODE_TYPES.C:
        // handle cat node
        return d.x - 50;
      default:
        return d.x;
    }
  })
  .attr("y", d => d.y)

// loop thru tree to look for overlap
function checkOverlap(node) {

}