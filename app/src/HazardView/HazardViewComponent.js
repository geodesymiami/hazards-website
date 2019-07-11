import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";
import ImageTypeTabs from "./components/Tabs";
import axios from "axios";

export default class HazardViewComponent extends Component {

  constructor(props) {
        super(props);
        this.state = {
            image_types: [],
            images_by_satellite: []
        }
  }

  componentDidUpdate(prevProps) {

  }

  componentDidMount() {
        var id = this.props.haz_id

        axios.get(`http://0.0.0.0:5000/api/volcano/images/${id}`, {mode: "cors"})
            .then((response) => {
                var available_image_types = Object.keys(response.data["images_by_type"])
                var available_images = response.data["images_by_type"]
                this.setState({
                    image_types: available_image_types,
                    images_by_satellite: available_images
                })
            })
  }

  render() {
        return (
            <div className="HazardViewComponent container-fluid">
                <Header id={this.props.haz_id}/>
                <ImageTypeTabs image_types={this.state.image_types} haz_id={this.props.haz_id} images={this.state.images_by_satellite}/>
            </div>
        );
  }
}
