import React, { Component } from "react";
import "./HazardViewComponent.css";
import Header from "./components/Header";

export default class HazardViewComponent extends Component {

  constructor(props) {
    super(props);
  }

  componentDidUpdate(prevProps) {

  }

  componentDidMount() {
    console.log(this.props.id)
  }

  render() {
    return (
        <div className="HazardViewComponent container-fluid">
            <Header id={this.props.id} />
        </div>
    );
  }
}
