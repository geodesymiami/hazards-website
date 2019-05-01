import React, { Component } from "react";
import "./Images.css";
import axios from "axios";

class Images extends Component {
  constructor(props) {
    super(props);

    this.state = {
      filter: this.props.filter,
      imageData: null
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ filter: nextProps.filter });
  }

  componentDidMount() {
    var id = this.props.id;
    axios
      .get("/api/volcanoes/" + id)
      .then(response => {
        this.setState({
          imageData: response.data.images_by_satellite
        });
      })
      .catch(error => console.log(error));
  }

  printThumbnail = element => (
    <div class="col col-sm-auto col-md-auto col-lg-auto" key={Math.random()}>
      <img
        src={element.compressed_image_url}
        class="img-thumbnail"
        alt="Image"
      />
    </div>
  );

  printName = type => {
    switch (type) {
      case "geo_backscatter":
        return "Georectified Backscatter";
      case "geo_coherence":
        return "Georectified Coherence";
      case "geo_interferogram":
        return "Georectified Interferogram";
      case "ortho_backscatter":
        return "Orthorectified Backscatter";
      case "ortho_coherence":
        return "Orthorectified Coherence";
      case "ortho_interferogram":
        return "Orthorectified Interferogram";
    }
  };

  printRow = (satellite, type) => (
    <div class="image-type-section" key={satellite + this.printName(type)}>
      <h3>{this.printName(type)}</h3>
      <div class="row">{satellite[type].map(this.printThumbnail)}</div>
    </div>
  );

  printRows = satellite => {
    var rtrn = [];

    if (this.state.filter.Backscatter && this.state.filter.Georectified) {
      rtrn.push(this.printRow(satellite, "geo_backscatter"));
    }

    if (this.state.filter.Interferogram && this.state.filter.Georectified) {
      rtrn.push(this.printRow(satellite, "geo_interferogram"));
    }

    if (this.state.filter.Coherence && this.state.filter.Georectified) {
      rtrn.push(this.printRow(satellite, "geo_coherence"));
    }

    if (this.state.filter.Backscatter && this.state.filter.Orthorectified) {
      rtrn.push(this.printRow(satellite, "ortho_backscatter"));
    }

    if (this.state.filter.Interferogram && this.state.filter.Orthorectified) {
      rtrn.push(this.printRow(satellite, "ortho_interferogram"));
    }

    if (this.state.filter.Coherence && this.state.filter.Orthorectified) {
      rtrn.push(this.printRow(satellite, "ortho_coherence"));
    }

    return rtrn;
  };

  createSatelliteSection = (satName, satellite) => (
    <div class="satellite-section" key={satName}>
      <h2>{satName}</h2>
      {this.printRows(satellite)}
    </div>
  );

  createSatelliteSections = () => {
    var rtrn = [];
    for (var satellite in this.state.imageData) {
      rtrn.push(
        this.createSatelliteSection(satellite, this.state.imageData[satellite])
      );
    }
    return rtrn;
  };

  render() {
    if (!this.state.imageData) {
      return <div />;
    }
    return (
      <div id="ImgBoundingBox" class="container-fluid main">
        {this.createSatelliteSections()}
      </div>
    );
  }
}

export default Images;
