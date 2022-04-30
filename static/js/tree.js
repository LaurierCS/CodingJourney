// d3 dummy tree test

const treeData = [
  { id: "root", label: "Root", isRoot: true },
  { id: "child-a", label: "child a", parentId: "root", isChild: true },
  { id: "child-b", label: "child b", parentId: "root" },
  { id: "child-a-a", label: "child a of a", parentId: "child-a" },
]

const margin = {top: 20, right: 90, bottom: 30, left: 90},
      width  = 660 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

const treeLayout = d3.tree().size([1280, 500])
let hierarchy = d3.stratify()(treeData)
let nodes = d3.hierarchy(hierarchy, d => {
  // console.log(d)
  return d.children
})
nodes = treeLayout(nodes)

const container = d3.select("#treeContainer")

const svg = container.append("svg")
.attr("width", "100%")
.attr("height", "100vh")

const links = hierarchy.links()

const link = svg
  .selectAll(".link")
  .data(nodes.links())
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", d => {
    console.log(d.target)
    d.target.y += 70
    let y = d.target.y + 300
    return "M" + y + "," + d.target.x
    + "C" + (d.target.y + d.source.y) / 2 + "," + d.target.x
    + " " + (d.target.y + d.source.y) / 2 + "," + d.source.x
    + " " + d.source.y + "," + d.source.x;
  })

const node = svg.selectAll(".node")
  .data(nodes.descendants())
  .enter()
  .append("g")
  .attr("class", d => d.data.isRoot ? "node-root" : "node")
  .attr("transform", d => "translate(" + d.y + "," + d.x + ")")

node.append("rect")
  .attr("class", "node") // we could substitute this with the style attribute
  .attr("rx", "15")
  .attr("ry", "15")

node.append("image")
  .attr("class", "node-image")
  .attr("width", "120")
  .attr("height", "120")
  .attr("href", "/static/images/python_logo.png") // here we could load the image with base64
  .attr("x", "13")
  .attr("y", "13")

const arcGenerator = d3.arc()
  .outerRadius(22)
  .innerRadius(0)
  .startAngle(-Math.PI / 2)
  .endAngle(Math.PI / 2);

const arc = node.append("path")
  .attr("transform", "translate(0,0)")
  .attr("d", arcGenerator())
  .attr("fill", "red")
  .attr("stroke", "none")

// node.append()

// node.append("path") // half circle, top part
//   .attr("d", d => {
//     return "M120,120 a60,60 0 1,0 120,0"
//   })
//   .attr("fill", "#475aaa")


// const svg = d3
//   .select("svg")
//   .attr("width", "100%") 
//   .attr("height", "500")
//   .attr("cursor", "grab")
//   .attr("position", "relative")


const skills = [
  {id: "languages", label:"Languages",},
  {
    parentId: "languages",
    id: "python",
    label: 'Python', 
    iconHref: require('pod\static\images\python_logo.png'), 
    skillLevel: 4.5, 
    descrption: ["I'm the best python programmer that's ever pythoned"]
  }, 
  {
    parentId: "python",
    id: "django",
    label: 'Django', 
    iconHref: require('pod\static\images\python_logo.png'), 
    skillLevel: 3, 
    descrption: ["I'm alright at django"]
  }
]

let hierarchy2 = d3.stratify() (this.skills);