/**
 * Class based skill tree will allow the flexibility to have one or more
 * trees in a view without a lot of trouble.
 * This class should be used as a way to create a new skill tree.
 * 
 * @param {string} username desired skill tree of user
 * @param {string} container a valid selector string that is usable by jquery
 * @param {boolean} editable control whether the user viewing the skill tree is allowed to edit of skills.
 * @constuctor
 */

class SkillTree {
  // STATIC VARIABLES
  /**
   * @constant
   * Different of node types.
   * C -> Category;
   * U -> User;
   * N -> Node;
   */
  NODE_TYPES = {
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
  NODE_DIM = {
    C: [250, 60],
    N: [150, 150],
    U: [150, 150],
  };

  /**
   * @constant
   */
  NODE_IMG_SIZE = 120

  TOUCHPAD_TIMEOUT = 50; // milliseconds

  ZOOM_EVENT_MAX_TRIGGERS = 10; // 1/10ms

  ZOOM_TOUCHPAD_RATIO = 0.01;

  ZOOM_WHEEL_RATIO = 0.1;

  constructor(username, container_selector) {
    this.username = username;
    this.container_selector = container_selector;

    this.is_owner = false;

    // get container dimensions
    this.container = $(this.container_selector);
    this.container_width = this.container.width();
    this.container_height = this.container.height();
    
    $(window).resize(this._on_window_resize.bind(this));

    // set the viewbox to control zoom/padding
    this.viewbox = {
      x: -this.container_width / 2 - this.NODE_DIM.U[0] * 2,
      y: 0,
      width: this.container_width * 1.5, // zoom out view
      height: this.container_height * 1.5, // zoom out view
    }

    // variables to keep track of padding and zooming
    this._origin_point = {
      x: -1,
      y: -1,
    };
    this._new_viewbox = { ...this.viewbox }
    this._is_pointer_down = false;

    this.tree_data = null;
    this.profile_picture_url = "";

    // padding, moving skill tree
    this._is_pointer_down = false;

    // variables to assist when determining touchpad or wheel zoom
    this._zoom_start = -1;
    this._zoom_event_count = 0;
    this.is_touchpad_defined = false;
    this.is_touchpad = false;
  }

  async _get_skills() {
    // make http get request for tree data in json format
    try {
      const res = await fetch('/skill-tree-data?username='+this.username);
      const { data, is_owner } = await res.json();
      const skills = JSON.parse(data);

      this.is_owner = is_owner;

      if (skills.length < 1) return [];

      let i;
      for (i=0;i<skills.length;i++) {
        skills[i].parentId = skills[i].parentId_id;
        skills[i].nodeType = skills[i].node_type;
        delete skills[i].parentId_id
        delete skills[i].node_type
      }

      this.profile_picture_url = skills[0].icon_HREF ?? "";

      return skills

    } catch (error) {
      console.error('Error getting skills.')
      console.error(error)
    }
  }

  _get_link_path(d) {
    const halfNodeSize = this.NODE_DIM.N[0] / 2;

    // We want the links from the User Node to start from the center of the node instead of the top.
    if (d.source.data.nodeType === this.NODE_TYPES.U) {
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

  _get_viewbox_string(x, y, w, h) {
    return `${x} ${y} ${w} ${h}`;
  }

  async create_tree() {
    
    if (this.tree_data === null) {
      this.tree_data = await this._get_skills();
    }

    if (this.profile_picture_url.length < 1) {
      this.profile_picture_url = await this._get_profile_picture(true);
    }

    this.container_d3 = d3.select(this.container_selector);

    this.treemap = d3.tree()
    .size([this.container_height, this.container_width])
    .nodeSize([225, 300])
    .separation((a, b) => {
      // todo: determine the space between category nodes based on the lenght of the labels.
      if (
        a.parent === b.parent &&
        a.data.nodeType === this.NODE_TYPES.C &&
        b.data.nodeType === this.NODE_TYPES.C
      ) {
        return 2;
      }

      return 1;
    });

    this.hierarchy = this.treemap(d3.stratify()(this.tree_data));
    this.descendants = this.hierarchy.descendants();

    this.d3_svg = this.container_d3
    .append("svg")
    .attr("id", "tree")
    .attr("width", this.container_width)
    .attr("height", this.container_height)
    .attr("style", "cursor: move;")
    .attr("viewBox", this._get_viewbox_string(this.viewbox.x, this.viewbox.y, this.viewbox.width, this.viewbox.height)); // for zooming in/out

    this.d3_defs = this.d3_svg.append("defs");
    this.d3_defs
    .append("clipPath")
    .attr("id", "user-clip")
    .append("rect")
    .attr("width", this.NODE_DIM.U[0])
    .attr("height", this.NODE_DIM.U[1])
    .attr("rx", this.NODE_DIM.U[0]/2)
    .attr("ry", this.NODE_DIM.U[0]/2);

    this.tree = this.d3_svg.append("g").attr("data-tree", "true");

    this.links = this.tree
    .selectAll(".link") 
    .data(this.hierarchy.links())
    .enter()
    .append("path")
    .attr("class", "link")
    .attr("d", (d) => this._get_link_path(d))

    this.nodes = this.tree
    .selectAll(".node")
    .data(this.descendants)
    .enter()
    .append("g")
    .attr("class", "node-group")
    .on("click", this._on_node_click.bind(this));

    this.rects = this.nodes
    .append("rect")
    .attr("class", (d) =>
    d.data.nodeType === this.NODE_TYPES.C ? "node-category" : d.data.nodeType === this.NODE_TYPES.U ? "node node-user" : "node"
    )
    .attr("width", (d) => this.NODE_DIM[d.data.nodeType][0])
    .attr("height", (d) => this.NODE_DIM[d.data.nodeType][1])
    .attr("rx", (d) => (d.data.nodeType === this.NODE_TYPES.U ? this.NODE_DIM.U[0]/2 : 15))
    .attr("ry", (d) => (d.data.nodeType === this.NODE_TYPES.U ? this.NODE_DIM.U[0]/2 : 15))
    .attr("x", (d) => d.data.nodeType === this.NODE_TYPES.C ? d.x - 50 : d.x )
    .attr("y", (d) => d.y)
    .attr("data-node-id", d => d.id);

    this.node_labels = this.nodes
    .append("text")
    .text(d => {
      if (d.data.nodeType === this.NODE_TYPES.U && this.username) {
        return this.username;
      }
  
      return d.data.name;
    })
    .attr("class", d => d.data.nodeType !== this.NODE_TYPES.C ? "node-label" : "node-label node-title")
    .attr("x", d => {
      // because the x in d.x does not reflect the x position of the rectangle
      // to center the text for a category node, we need to get the x from the rect element directly.
      let x;
      if (d.data.nodeType === this.NODE_TYPES.C) {
        let r = document.querySelector(`rect[data-node-id="${d.id}"`)
        x = parseFloat(r.getAttribute("x"))
      } else {
        x = d.x
      }
      return x + this.NODE_DIM[d.data.nodeType][0] / 2;
    })
    .attr("y", d => d.data.nodeType === this.NODE_TYPES.C ? d.y + this.NODE_DIM.C[1] / 2 : d.y + this.NODE_DIM[d.data.nodeType][1] + 20)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .attr("data-node-label-id", d => d.id);

    this.node_images = this.nodes
    .append("image")
    .attr("href", d => {  
      if (d.data.nodeType === this.NODE_TYPES.U) {
        return this.profile_picture_url;
      }
  
      return "/static/images/svg/badge.svg" // todo: change to return actual icon when available
    })
    .attr("class", "node-image")
    .attr("width", d => {

      let width = 0;

      switch (d.data.nodeType) {
        case "U":
          width = this.NODE_DIM.U[0];
          break;
        case "N":
          width = this.NODE_IMG_SIZE;
          break;
        default:
          break;
      }

      return width;
    })
    .attr("height", d => {
      let height = 0;

      switch (d.data.nodeType) {
        case "U":
          height = this.NODE_DIM.U[1];
          break;
        case "N":
          height = this.NODE_IMG_SIZE;
          break;
        default:
          break;
      }

      return height;
    })
    .attr("x", d => d.x + this.NODE_DIM[d.data.nodeType][0] / 2 - (d.data.nodeType === this.NODE_TYPES.N ? this.NODE_IMG_SIZE : this.NODE_DIM.U[0]) / 2)
    .attr("y", d => d.y + this.NODE_DIM[d.data.nodeType][1] / 2 - (d.data.nodeType === this.NODE_TYPES.N ? this.NODE_IMG_SIZE : this.NODE_DIM.U[1]) / 2)
    .attr("clip-path", d => d.data.nodeType === this.NODE_TYPES.U ? "url(#user-clip)" : "")
    .attr("preserveAspectRatio", "xMidYMid slice")
    .attr("data-node-image-id", d => d.id);


    await this._enable_tree_interactions();
  }

  async _get_profile_picture(fetch_by_username = false) {
    try {
      if (this.is_owner && fetch_by_username) {

        const res = await fetch('/user-profile-picture?username='+this.username);
  
        const { url } = await res.json();

        return url;
      }
      
      return this.tree_data[0].icon_HREF;

    } catch (error) {
      console.error("Error getting profile picture.")
      console.error(error);
    }
  }

  _get_point(e) {
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
  
  _on_pointer_down(e) {
    e.preventDefault()
    this._is_pointer_down = true;
    let point = this._get_point(e);
    this._origin_point.x = point.x;
    this._origin_point.y = point.y;
  }
  
  _on_pointer_up(e) {
    e.preventDefault()
    this._is_pointer_down = false;
  
    this.viewbox.x = this._new_viewbox.x;
    this.viewbox.y = this._new_viewbox.y;
  }
  
  _on_pointer_move(e) {
    if (!this._is_pointer_down) return;
  
    e.preventDefault();
    let cursor_position = this._get_point(e);
  
    this._new_viewbox.x = this.viewbox.x - (cursor_position.x - this._origin_point.x);
    this._new_viewbox.y = this.viewbox.y - (cursor_position.y - this._origin_point.y);
  
    let viewbox_string = this._get_viewbox_string(
      this._new_viewbox.x,
      this._new_viewbox.y,
      this.viewbox.width,
      this.viewbox.height
    );
    this._tree_svg_el.attr("viewBox", viewbox_string);
  }
  
  _on_zoom(e) {
    // do not let user zoom when panning.
    if (this._is_pointer_down) return;
    
    // touch pad triggers multiple events in a short period of time
    // causing zooming in/out to be fast and hard to control
    // this is a work around to determine if the user is using a touch pad or mouse wheel.
    // BUG: When zooming and the browser lags, it wrongly determines the type.
    if (!this.is_touchpad_defined) {
      if (this._zoom_event_count === 0) {
        this._zoom_start = Date.now();
      }

      this._zoom_event_count++;
      
      if (Date.now() - this._zoom_start > this.TOUCHPAD_TIMEOUT) {
        if (this._zoom_event_count > this.ZOOM_EVENT_MAX_TRIGGERS) {
          this.is_touchpad = true
        }

        this.is_touchpad_defined = true;
        this._zoom_start = -1;
      }
      return;
    }
  
    // 1 for zoom in, -1 for zoom out
    let sign = Math.sign(e.originalEvent.deltaY);
    let zoomRatioWidth = this.viewbox.width * (this.is_touchpad ? this.ZOOM_TOUCHPAD_RATIO : this.ZOOM_WHEEL_RATIO);
    let zoomRatioHeight = this.viewbox.height * (this.is_touchpad ? this.ZOOM_TOUCHPAD_RATIO : this.ZOOM_WHEEL_RATIO);
  
    if (sign < 0) {
      // zoom out
      this.viewbox.width = this.viewbox.width - zoomRatioWidth;
      this.viewbox.height = this.viewbox.height - zoomRatioHeight;
    } else {
      this.viewbox.width = this.viewbox.width + zoomRatioWidth;
      this.viewbox.height = this.viewbox.height + zoomRatioHeight;
    }
    this._tree_svg_el.attr(
      "viewBox",
      this._get_viewbox_string(this.viewbox.x, this.viewbox.y, this.viewbox.width, this.viewbox.height)
    );
  }

  _on_node_click(e, d) {

    // assert if a node side bar has been included in the page
    if (NodeSideBar === undefined) return;

    if (d.data.nodeType === this.NODE_TYPES.U || d.data.nodeType === this.NODE_TYPES.C) {
      return;
    }
  
    // check if sidebar exists or not
    if (!this.node_side_bar && NodeSideBar !== undefined) {
      this.node_side_bar = new NodeSideBar("nsb", this.is_owner)
    }
  
    this.node_side_bar.show(d);
  }

  async _enable_tree_interactions() {
    if (!this._tree_svg_el)
      this._tree_svg_el = $("#tree");
    if (window.PointerEvent) {
      this._tree_svg_el.on("pointerdown", this._on_pointer_down.bind(this));
      this._tree_svg_el.on("pointerup", this._on_pointer_up.bind(this));
      this._tree_svg_el.on("pointerleave", this._on_pointer_up.bind(this));
      this._tree_svg_el.on("pointermove", this._on_pointer_move.bind(this));
    } else {
      // Add all mouse events listeners fallback
      this._tree_svg_el.on("mousedown", this._on_pointer_down.bind(this));
      this._tree_svg_el.on("mouseup", this._on_pointer_up.bind(this));
      this._tree_svg_el.on("mouseleave", this._on_pointer_up.bind(this));
      this._tree_svg_el.on("mousemove", this._on_pointer_move.bind(this));
    
      // Add all touch events listeners fallback
      this._tree_svg_el.on("touchstart", this._on_pointer_down.bind(this));
      this._tree_svg_el.on("touchend", this._on_pointer_up.bind(this));
      this._tree_svg_el.on("touchmove", this._on_pointer_move.bind(this));
    }

    this._tree_svg_el.on("wheel", this._on_zoom.bind(this));
  }

  _on_window_resize() {
    if (this.container.length > 0) {
      this.container_width = this.container.width();
      this.container_height = this.container.height();

      this._tree_svg_el.attr("width", this.container_width);
      this._tree_svg_el.attr("height", this.container_height);
      this._tree_svg_el.attr(
        "viewBox",
        this._get_viewbox_string(this.viewbox.x, this.viewbox.y, this.viewbox.width, this.viewbox.height)
      );
    }
  }
}