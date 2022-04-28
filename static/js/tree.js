// d3 dummy tree test

const treeData = [
  { id: "root", label: "Root", isRoot: true },
  { id: "child-a", label: "child a", parentId: "root", isChild: true },
  { id: "child-b", label: "child b", parentId: "root" },
  { id: "child-a-a", label: "child a of a", parentId: "child-a" } 
]

const margin = {top: 20, right: 90, bottom: 30, left: 90},
      width  = 660 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

const treeLayout = d3.tree().size([1280, 500])
let hierarchy = d3.stratify()(treeData)
let nodes = d3.hierarchy(hierarchy, d => {
  console.log(d)
  return d.children
})
nodes = treeLayout(nodes)

const container = d3.select("#tree_container")

const svg = container.append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)

const g = svg.append("g")

const link = g
  .selectAll(".link")
  .data(nodes.descendants().slice(1))
  .enter()
  .append("path")
  .attr("class", "link")
  .attr("d", d => {
    return "M" + d.y + "," + d.x
    + "C" + (d.y + d.parent.y) / 2 + "," + d.x
    + " " + (d.y + d.parent.y) / 2 + "," + d.parent.x
    + " " + d.parent.y + "," + d.parent.x;
  })

const node = g.selectAll(".node")
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


  