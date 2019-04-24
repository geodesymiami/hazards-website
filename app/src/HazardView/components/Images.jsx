import React, { Component } from "react";
import "./Images.css";
import Container from "react-bootstrap/Container";

class Images extends Component {
  state = {};
  render() {
    return (
      <div id="ImgBoundingBox" class="container-fluid main">
        <div class="row">
          <div class="col">
            <h1>Image 1</h1>
          </div>
          <div class="col">
            <h1>Image 2</h1>
          </div>
          <div class="col">
            <h1>Image 3</h1>
          </div>
        </div>
      </div>
    );
  }
}

export default Images;
