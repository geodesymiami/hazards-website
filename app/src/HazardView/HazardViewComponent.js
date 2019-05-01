import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Images from "./components/Images";

const IMAGETYPE = ["Backscatter", "Interferogram", "Coherence"];
const RECTIFICATION = ["Georectified", "Orthorectified"];

const FILTER = IMAGETYPE.concat(RECTIFICATION);

export default class HazardViewComponent extends Component {
  /*
  TODO: Add Satellite Options
 */

  constructor(props) {
    super(props);
    this.state = {
      hazardId: this.props.hazardId,
      filter: FILTER.reduce(
        (options, option) => ({
          ...options,
          [option]: true
        }),
        {}
      )
    };

    this.filterHandler = this.filterHandler.bind(this);
  }

  filterHandler(filterToChange, value) {
    this.setState(prevState => ({
      hazardId: prevState.hazardId,
      filter: {
        ...prevState.filter,
        [filterToChange]: value
      }
    }));
    console.log(filterToChange + " is " + value);
  }

  getParams(location) {
    const searchParams = new URLSearchParams(location.location.search);
    var { filterData } = {};

    filterData = [];
    filterData.push(searchParams.get("imageType"));
    filterData.push(searchParams.get("rectification"));
    return filterData;
  }

  setParams({ imageType = "", rectification = "" }) {
    const searchParams = new URLSearchParams();
    searchParams.set("imageType", imageType);
    searchParams.set("rectification", rectification);
    return searchParams.toString();
  }

  getUpdateURL = () => {
    var imgTypes = "";
    var rects = "";
    IMAGETYPE.forEach(type => {
      if (this.state.filter[type]) {
        imgTypes = imgTypes.concat(type);
        imgTypes = imgTypes.concat(",");
      }
    });

    RECTIFICATION.forEach(type => {
      if (this.state.filter[type]) {
        rects = rects.concat(type);
        rects = rects.concat(",");
      }
    });

    const url = this.setParams({ imageType: imgTypes, rectification: rects });
    return `?${url}`;
  };

  componentDidUpdate(prevProps) {
    const url = this.getUpdateURL();
    if (url !== prevProps.location.search) {
      this.props.navigate(url);
      console.log("URL Updating");
    }
  }

  updateFilters(filterData) {
    var options = [];
    filterData.forEach(string => {
      if (string != null) {
        options = options.concat(string.split(","));
      }
    });

    if (options.length > 0) {
      Object.keys(this.state.filter).forEach(checkbox => {
        this.filterHandler(checkbox, false);
      });

      options.forEach(checkbox => {
        this.filterHandler(checkbox, true);
      });
    }
  }

  componentDidMount() {
    const filter = this.getParams(this.props);
    this.updateFilters(filter);
  }

  render() {
    return (
      <div className="HazardViewComponent container-fluid">
        <div class="row">
          <div class="sidebar">
            <Sidebar
              action={this.filterHandler}
              checkboxes={this.state.filter}
              location={this.props}
            />
          </div>
          <div class="col-sm-12">
            <Header id={this.state.hazardId} />
            <Images id={this.state.hazardId} filter={this.state.filter} />
          </div>
        </div>
      </div>
    );
  }
}
