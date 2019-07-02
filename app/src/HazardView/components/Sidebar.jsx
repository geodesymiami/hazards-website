import React, { Component } from "react";
import "./Sidebar.css";
import {Form, Col, InputGroup} from "react-bootstrap"

const IMAGETYPE = ["Backscatter", "Interferogram", "Coherence"];
const RECTIFICATION = ["Georectified", "Orthorectified"];

class Sidebar extends Component {

  constructor(props){
    super(props)
  }

  render() {
    return (
      <div className="sidebar">
        <div className="nav-sidebar">
          <form>
            <h3>Filter Options</h3>
            <Form.Group controlId="exampleForm.ControlSelect1">
              <Form.Label>Satellite</Form.Label>
              <Form.Control as="select" multiple>
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername">
              <Form.Label>Start Date</Form.Label>
              <InputGroup>
                <InputGroup.Prepend>
                  <InputGroup.Text id="startDatePre">@</InputGroup.Text>
                </InputGroup.Prepend>
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="startDatePre" />
                <Form.Control.Feedback type="invalid">
                  Please choose a username.
                </Form.Control.Feedback>
              </InputGroup>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername">
              <Form.Label>End Date</Form.Label>
              <InputGroup>
                <InputGroup.Prepend>
                  <InputGroup.Text id="endDatePre">@</InputGroup.Text>
                </InputGroup.Prepend>
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="endDatePre" />
                <Form.Control.Feedback type="invalid">
                  Please choose a username.
                </Form.Control.Feedback>
              </InputGroup>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control as="select">
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
              </Form.Control>
              <Form.Label>images</Form.Label>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control as="select">
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
              </Form.Control>
              <Form.Label>days</Form.Label>
            </Form.Group>
          </form>
        </div>
      </div>
    );
  }
}

export default Sidebar;
