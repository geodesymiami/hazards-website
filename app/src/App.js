import React, { Component } from 'react';
import { Navbar, Nav,Container } from 'react-bootstrap'
import { Router} from '@reach/router'
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
                    <Nav.Link href="/list">Volcanos List</Nav.Link>
                    <Nav.Link href="/map">Volcanos Map</Nav.Link>
                    <Nav.Link href="#home" disabled>Earthquakes List</Nav.Link>
                    <Nav.Link href="#link" disabled>Earthquakes Map</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>

        <Container>
            <Router>
              <HomeViewComponent path="/" noThrow />
              <ListViewComponent path="/list" />
              {/*<Redirect to={"/volcanos/list"} from={"/volcanos"} noThrow />*/}
              <MapViewComponent path="/map" />
              <HazardViewComponent path="/hazard/:id" />
              <FourOhFourViewComponent default />
            </Router>
        </Container>
      </div>
    );
  }
}

export default App;
