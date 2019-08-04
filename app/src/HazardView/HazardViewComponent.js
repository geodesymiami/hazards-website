import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";
import ImageTypeTabs from "./components/Tabs";
import axios from "axios";
import queryString from "query-string"

export default class HazardViewComponent extends Component {

  constructor(props) {
        super(props);
        this.state = {
            active_image_type: '',
            image_types: [],
            images_by_satellite: [],
            url_params: {}
        }

        this.getImages = this.getImages.bind(this)
  }

  componentDidUpdate(prevProps) {

  }

  componentDidMount() {
      // Get and format URL variables here
      const url_params = queryString.parse(this.props.location.search)

      var img_type = url_params['img_type'] !== undefined ? url_params['img_type'] : ''
      var satellites = url_params['satellites'] !== undefined ? url_params['satellites'] : '';
      var start_date = url_params['start_date'] !== undefined ? url_params['start_date'] : '';
      var end_date = url_params['end_date'] !== undefined ? url_params['end_date'] : '';
      var max_imgs = url_params['max_num_images'] !== undefined ? url_params['max_num_images'] : '';
      var last_days = url_params['last_n_days'] !== undefined ? url_params['last_n_days'] : '';

      this.setState({
          active_image_type: img_type
      })

      var data = {
          "satellites": satellites,
          "start_date": start_date,
          "end_date": end_date,
          "max_num_images": max_imgs,
          "last_n_days": last_days
      }
      this.setState({
          url_params: data
      })

      console.log(this.state.active_image_type)

      this.getImages(data)
  }

  getImages(data){

      const queryString = new URLSearchParams(data).toString()

      axios.get(`http://0.0.0.0:5000/api/volcano/images/${this.props.haz_id}?${queryString}`, {mode: "cors"})
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

                <ImageTypeTabs image_types={this.state.image_types}
                               active_image_type={this.state.active_image_type}
                               haz_id={this.props.haz_id}
                               images={this.state.images_by_satellite}
                               filter_func={this.getImages}
                               url_data={this.state.url_params}
                />

            </div>
        );
  }
}
