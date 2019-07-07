import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";
import ImageTypeTabs from "./components/Tabs";

export default class HazardViewComponent extends Component {

  constructor(props) {
    super(props);
    this.state = {
      image_types: ["All", "Geo Backscatter", "Geo Coherence", "Geo Interferogram",
                    "Ortho Backscatter", "Ortho Coherence", "Ortho Interferogram"]
    }
  }

  componentDidUpdate(prevProps) {

  }

  componentDidMount() {
    console.log(this.props.id)
  }

  render() {
    return (
        <div className="HazardViewComponent container-fluid">
            <Header id={this.props.haz_id} />
            <ImageTypeTabs image_types={this.state.image_types} haz_id={this.props.haz_id}/>
        </div>
    );
  }
}
