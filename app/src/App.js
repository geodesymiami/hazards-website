import React, { Component } from 'react';
import { Navbar, Nav } from 'react-bootstrap'
import { Router, Location, navigate, Redirect } from '@reach/router'
import ListViewComponent from './ListView/ListViewComponent'
import MapViewComponent from './MapView/MapViewComponent'
import HazardViewComponent from './HazardView/HazardViewComponent'
import './App.css';
import FourOhFourViewComponent from './404View/404ViewComponent';

class App extends Component {
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
          <MapViewComponent     path="/map"  />
          <HazardViewComponent  path="/hazard" />
          <FourOhFourViewComponent default />
        </Router>
      </div>
    );
  }
}

export default App;
