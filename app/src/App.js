import React, { Component } from 'react';
import { Navbar, Nav,Container } from 'react-bootstrap'
import { Router, Redirect } from '@reach/router'
import ListViewComponent from './ListView/ListViewComponent'
import MapViewComponent from './MapView/MapViewComponent'
import HazardViewComponent from './HazardView/HazardViewComponent'
import HomeViewComponent from './HomeView/HomeViewComponent'
import './App.css';
import FourOhFourViewComponent from './404View/404ViewComponent';


class App extends Component {

  componentDidMount() {

  }

  render() {
    return (
      <div>
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="/"><b>RSMAS GeoHazards</b></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="/volcanos/list">Volcanos List</Nav.Link>
                    <Nav.Link href="/volcanos/map">Volcanos Map</Nav.Link>
                    <Nav.Link href="#home" disabled>Earthquakes List</Nav.Link>
                    <Nav.Link href="#link" disabled>Earthquakes Map</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>

        <div className={"container-fluid"}>
            <Router>
              <HomeViewComponent path="/" noThrow />
              <ListViewComponent path="/volcanos/list" />
              <Redirect to={"/volcanos/list"} from={"/volcanos"} noThrow />
              <MapViewComponent path="/volcanos/map" />
              <HazardViewComponent path="/volcanos/:haz_id" />
              <FourOhFourViewComponent default />
            </Router>
        </div>
      </div>
    );
  }
}

export default App;
