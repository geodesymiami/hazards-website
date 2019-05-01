import React, { Component } from "react";
import "./Header.css";
import axios from "axios";

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      hazardName: "",
      longitude: "",
      latitude: ""
    };
  }

  componentDidMount() {
    var id = this.props.id;

    axios
      .get("/api/volcanoes/" + id)
      .then(response =>
        this.setState({
          hazardName: response.data.hazard_name,
          longitude: response.data.location.longitude,
          latitude: response.data.location.latitude
        })
      )
      .catch(error => console.log(error));
  }

  render() {
    return (
      <div id="HazardInfo" class="hazardinfo">
        <h1>{this.state.hazardName}</h1>
        <h6>Hazard Id: {this.props.id}</h6>
        <h6>Latitude: {this.state.latitude}</h6>
        <h6>Longitude: {this.state.longitude}</h6>
        <h6>Elevation: </h6>
      </div>
    );
  }
}

export default Header;
