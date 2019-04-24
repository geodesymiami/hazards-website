import React, { Component } from 'react';
import { Navbar, Nav } from 'react-bootstrap'
import { Router, Location, navigate, Redirect } from '@reach/router'
import ListViewComponent from './ListView/ListViewComponent'
import MapViewComponent from './MapView/MapViewComponent'
import HazardViewComponent from './HazardView/HazardViewComponent'
import './App.css';
import FourOhFourViewComponent from './404View/404ViewComponent';
// HazardView team's npm modules
import axios from "axios";

class App extends Component {

 // default State object for entire app
 state = {
  volcanoes: [],
  earthquakes: []
};

componentDidMount(){

  // fetching Volcanoes data
  axios
  .get("<url.com>/api/volcanoes")
  .then(response => {
    const newVolcanoes = response.data.hazards.map( volcano => {
      return {
        id: volcano.hazard_id,
        last_updated: volcano.last_updated,
        name: volcano.name,
        link: `<url.com>/api/volcanoes/${volcano.hazard_id}`,
        coordinates: [volcano.location.latitude, volcano.location.longitude]
      };
    });

    const newState = Object.assign({}, this.state, {
      volcanoes: newVolcanoes
    });

    this.setState(newState);
  })
  .catch(error => console.log(error));

  // fetching Earthquakes data
  axios
  .get("<url.com>/api/earthquakes")
  .then(response => {
    const newVolcanoes = response.data.hazards.map( earthquake => {
      return {
        id: earthquake.hazard_id,
        last_updated: earthquake.last_updated,
        name: earthquake.name,
        link: `<url.com>/api/earthquakes/${earthquake.hazard_id}`,
        coordinates: [earthquake.location.latitude, earthquake.location.longitude]
      };
    });

    const newState = Object.assign({}, this.state, {
      earthquakes: newEarthquakes
    });

    this.setState(newState);
  })
  .catch(error => console.log(error));
}


  render() {
    return (
      <div>
        <Navbar bg="light">
          <Navbar.Brand>RSMAS Geohazards</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse>
            <Location>
            {({ location }) => 
              <Nav variant="pills" activeKey={location.pathname} onSelect={selectedKey => navigate(selectedKey) }>
                <Nav.Item>
                  <Nav.Link eventKey="/list">List View</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                  <Nav.Link eventKey="/map">Map View</Nav.Link>
                </Nav.Item>
              </Nav>
            }
            </Location>
          </Navbar.Collapse>
        </Navbar>
        <Router>
          <Redirect from="/" to="/list" noThrow />
          <ListViewComponent    path="/list" />
          <MapViewComponent     path="/map" volcanoes={this.state.volcanoes} earthquakes={this.state.earthquakes}/>
          <HazardViewComponent  path="/hazard" />
          <FourOhFourViewComponent default />
        </Router>
      </div>
    );
  }
}

export default App;
