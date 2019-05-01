import React, { Component } from "react";
import "./Sidebar.css";
import Checkbox from "./Checkbox";

const IMAGETYPE = ["Backscatter", "Interferogram", "Coherence"];
const RECTIFICATION = ["Georectified", "Orthorectified"];

class Sidebar extends Component {
  constructor(props) {
    super(props);
  }

  selectAllCheckboxes = isSelected => {
    Object.keys(this.props.checkboxes).forEach(checkbox => {
      this.props.action(checkbox, isSelected);
    });
  };

  selectAll = () => this.selectAllCheckboxes(true);

  deselectAll = () => this.selectAllCheckboxes(false);

  handleCheckboxChange = changeEvent => {
    const { name } = changeEvent.target;
    this.props.action(name, !this.props.checkboxes[name]);
  };

  createCheckbox = option => (
    <Checkbox
      label={option}
      isSelected={this.props.checkboxes[option]}
      onCheckboxChange={this.handleCheckboxChange}
      key={option}
    />
  );

  createCheckboxes = option => option.map(this.createCheckbox);

  render() {
    return (
      <div class="sidebar">
        <div class="nav-sidebar">
          <form>
            <h3>Image Type</h3>
            {this.createCheckboxes(IMAGETYPE)}
            <h3>Rectification</h3>
            {this.createCheckboxes(RECTIFICATION)}

            <div className="form-group mt-2">
              <button
                type="button"
                className="btn btn-outline-primary mr-2"
                onClick={this.selectAll}
              >
                Select All
              </button>
              <button
                type="button"
                className="btn btn-outline-primary mr-2"
                onClick={this.deselectAll}
              >
                Deselect All
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

export default Sidebar;
