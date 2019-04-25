import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Images from "./components/Images";
import Table from "react-bootstrap/Table";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

export default class HazardViewComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: []
    };
  }

  render() {
    return (
      <div className="HazardViewComponent container-fluid">
        <div class="row">
          <div class="sidebar">
            <Sidebar />
          </div>
          <div class="col-sm-12">
            <Header id="01123" />
            <Images />
          </div>
        </div>
      </div>
    );
  }
}
