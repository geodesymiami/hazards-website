import React, { Component } from "react";
import "./Header.css";
import axios from "axios";
import { Jumbotron } from "react-bootstrap"

var moment = require('moment')

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
        hazardId: "",
        hazardName: "",
        longitude: "",
        latitude: "",
        numImages: "",
        lastImageDate: ""
    };
  }

  componentWillMount() {
      var id = this.props.id;

      axios.get(`http://0.0.0.0:5000/api/volcano/${id}`, {mode: 'cors'})
            .then( (response) => {
                this.setState({
                    hazardId: this.props.id,
                    hazardName: response.data.hazard_name,
                    longitude: response.data.location.longitude,
                    latitude: response.data.location.latitude,
                    lastImageDate: moment(response.data.last_updated).format("YYYY-MM-DD").toString(),
                    numImages: response.data.num_images
                })
                console.log(this.state)
            })
  }

  render() {
    return (
          <Jumbotron id="HazardInfo" className="hazardinfo" style={{textAlign: "center"}}>
              <h1 className={"important"}>{this.state.hazardName}</h1>
              <h6>Volcano Id: {this.state.hazardId}</h6>
              <h6>Volcanic Caldera</h6>
              <hr />
              <h5 id={"num_images"}>{this.state.numImages} Images &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;  Last Image: {this.state.lastImageDate}</h5>
          </Jumbotron>
    );
  }
}

export default Header;
