import React, { Component } from "react";
import "./Sidebar.css";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavItem from "react-bootstrap/NavItem";
import NavLink from "react-bootstrap/NavLink";

class Sidebar extends Component {
  state = {};
  render() {
    return (
      <div class="sidebar">
        <ul class="nav-sidebar">
          <li class="nav-title">Sort</li>
          <li class="nav-item">
            <a class="nav-link" href="#">
              Image Type
            </a>
            <ul>
              <li>BackScatter</li>
              <li>Interferogram</li>
              <li>Coherence</li>
            </ul>
          </li>
          <li>
            <a href="#">Viewing Geometry</a>
          </li>
          <li>
            <a href="#">Rectification</a>
          </li>
          <li>
            <a href="#">Satellie</a>
          </li>
        </ul>
      </div>
    );
  }
}

export default Sidebar;
