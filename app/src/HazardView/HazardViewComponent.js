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

        this.getImages = this.getImages.bind(this)
  }

  componentDidUpdate(prevProps) {

  }

  componentDidMount() {
        this.getImages({})
  }

  getImages(data){

      console.log("getImages called")

      const queryString = new URLSearchParams(data).toString()

      axios.get(`http://0.0.0.0:5000/api/volcano/images/${this.props.haz_id}?${queryString}`, {mode: "cors"})
            .then((response) => {
                console.log(response)
                var available_image_types = Object.keys(response.data["images_by_type"])
                var available_images = response.data["images_by_type"]
                this.setState({
                    image_types: available_image_types,
                    images_by_satellite: available_images
                })
            })
  }

  render() {
      console.log("Component rendered")
        return (
            <div className="HazardViewComponent container-fluid">
                <Header id={this.props.haz_id}/>
                <ImageTypeTabs image_types={this.state.image_types} haz_id={this.props.haz_id} images={this.state.images_by_satellite} filter_func={this.getImages}/>
            </div>
        );
  }
}
