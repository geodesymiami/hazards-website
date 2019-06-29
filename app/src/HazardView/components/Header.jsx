import React, { Component } from "react";
import "./Header.css";
import axios from "axios";
import {Jumbotron} from "react-bootstrap"

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
        hazardName: "",
        longitude: "",
        latitude: "",
        numImages: "10",
        lastImageDate: ""
    };
  }

  componentWillMount() {
    var id = this.props.id;

    fetch(`http://0.0.0.0:5000/api/volcano/${id}`, {mode: 'cors'})
        .then((response) => {
            return response.json()
        })
        .then((data) =>
            this.setState({
                hazardName: data.hazard_name,
                longitude: data.location.longitude,
                latitude: data.location.latitude,
                lastImageDate: data.last_updated
            })
        )
        .catch(error => console.log(error));
  }

  render() {
    return (
          <Jumbotron id="HazardInfo" className="hazardinfo" style={{textAlign: "center"}}>
              <h1 className={"important"}>{this.state.hazardName}</h1>
              <h5>Hazard Id: {this.props.id}</h5>
              <h3 id={"num_images"}>{this.state.numImages} Images</h3>
              <h5>{this.state.lastImageDate}</h5>
          </Jumbotron>
    );
  }
}

export default Header;
