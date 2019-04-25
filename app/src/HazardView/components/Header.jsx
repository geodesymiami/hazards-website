import React, { Component } from "react";
import "./Header.css";

class Header extends Component {
  render() {
    return (
      <div id="HazardInfo" class="hazardinfo">
        <h1>Hazard Name</h1>
        <h6>Hazard Id: {this.props.id}</h6>
        <h6>Latitude:</h6>
        <h6>Longitude:</h6>
        <h6>Elevation:</h6>
      </div>
    );
  }
}

export default Header;
