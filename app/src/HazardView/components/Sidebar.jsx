import React, { Component } from "react";
import "./Sidebar.css";
import {Form, InputGroup, Button} from "react-bootstrap"
import axios from 'axios'

class Sidebar extends Component {

  constructor(props){
    super(props)

    console.log("Sidebar constructor")

    this.state = {
      satellites: []
    }

    console.log(this.props.filter_func)

    this.filterImages = this.filterImages.bind(this)
  }

  componentWillMount() {
    axios.get(`http://localhost:5000/api/satellites/${this.props.haz_id}`, {mode: "cors"})
        .then((response) => {
                this.setState({
                  satellites: response["data"].map(sat => sat.satellite_name)
                })
            })
  }

  filterImages(event){
    event.preventDefault()
    const form = event.target;
    const data = new FormData(form);

    console.log(this.props)

    this.props.filter_func(data)

    // const queryString = new URLSearchParams(data).toString()
    //
    // console.log(queryString)
    //
    // axios.get(`http://0.0.0.0:5000/api/volcano/images/${this.props.haz_id}?${queryString}`,
    //     {
    //       mode: "cors",
    //       params: data
    //     })
    //     .then( (response) => {
    //       console.log(response)
    //     })

  }

  render() {
    return (
      <div className="sidebar">
        <div className="nav-sidebar">
          <form onSubmit={this.filterImages}>
            <h3>Filter Options</h3>
            <Form.Group controlId="exampleForm.ControlSelect1">
              <Form.Label>Satellite</Form.Label>
              <Form.Control as="select" name={"satellite"} multiple>
                {this.state.satellites.map( (sat, index) => {
                  return <option key={sat} value={sat}>{sat}</option>
                })}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername">
              <Form.Label>Start Date</Form.Label>
              <InputGroup>
                <InputGroup.Prepend>
                  <InputGroup.Text id="startDatePre">@</InputGroup.Text>
                </InputGroup.Prepend>
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="startDatePre" name={"start_date"} />
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
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="endDatePre" name={"end_date"} />
                <Form.Control.Feedback type="invalid">
                  Please choose a username.
                </Form.Control.Feedback>
              </InputGroup>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control type="text" placeholder="0" name={"max_num_images"} />
              <Form.Label>images</Form.Label>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control type="text" placeholder="0" name={"last_n_days"} />
              <Form.Label>days</Form.Label>
            </Form.Group>
            <Button type={"submit"}>Submit</Button>
          </form>
        </div>
      </div>
    );
  }
}

export default Sidebar;
