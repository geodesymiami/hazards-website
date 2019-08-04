import React, { Component } from "react";
import "./Sidebar.css";
import {Form, InputGroup, Button} from "react-bootstrap"
import axios from 'axios'

class Sidebar extends Component {

  constructor(props){
    super(props)

    console.log("Sidebar constructor")

    this.state = {
      satellites: [],
      url_params: {}
    }

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

  componentWillReceiveProps(nextProps, nextContext) {
      this.setState({
        url_params: nextProps.url_data
      })
  }

  filterImages(event){
    event.preventDefault()
    const form = event.target;
    const data = new FormData(form);

    var satellites = data.getAll("satellites")
    data.delete("satellites")
    data.append("satellites", satellites.join(","))

    this.props.filter_func(data)

  }

  render() {

    const filtered_start = this.state.url_params['start_date']
    const filtered_end = this.state.url_params['end_date']
    const filtered_num = this.state.url_params['max_num_images']
    const filtered_n_days = this.state.url_params['last_n_days']

    return (
      <div className="sidebar">
        <div className="nav-sidebar">
          <form onSubmit={this.filterImages}>
            <h3>Filter Options</h3>
            <Form.Group controlId="exampleForm.ControlSelect1">
              <Form.Label>Satellite</Form.Label>
              <Form.Control as="select" name={"satellites"} multiple>
                {
                  this.state.satellites.map( (sat, index) => {
                      const filtered_sats = this.state.url_params['satellites']
                      if(filtered_sats !== undefined && filtered_sats.includes(sat)){
                          return <option key={sat} value={sat} selected>{sat}</option>
                      }
                      return <option key={sat} value={sat}>{sat}</option>
                  })
                }
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername">
              <Form.Label>Start Date</Form.Label>
              <InputGroup>
                <InputGroup.Prepend>
                  <InputGroup.Text id="startDatePre">@</InputGroup.Text>
                </InputGroup.Prepend>
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="startDatePre" name={"start_date"} defaultValue={filtered_start}/>
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
                <Form.Control type="text" placeholder="YYYY-MM-DD" aria-describedby="endDatePre" name={"end_date"} defaultValue={filtered_end}/>
                <Form.Control.Feedback type="invalid">
                  Please choose a username.
                </Form.Control.Feedback>
              </InputGroup>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control type="text" placeholder="0" name={"max_num_images"} defaultValue={filtered_num}/>
              <Form.Label>images</Form.Label>
            </Form.Group>
            <Form.Group controlId="validationCustomUsername" className={"form-inline"}>
              <Form.Label>Last</Form.Label>
              <Form.Control type="text" placeholder="0" name={"last_n_days"} defaultValue={filtered_n_days}/>
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
