import React, { Component } from 'react';
import { Jumbotron, Button, Row, Col, Container } from 'react-bootstrap'
import './styles.css'

class HomeViewComponent extends Component{

    render(){
        return (
            <Container>
                 <Jumbotron>
                    <Row>
                        <Col lg={8} xs={12}>
                            <h1>RSMAS GeoHazards</h1>
                            <p>An interactive, self-updating web application for displaying GEOTIFF satellite images of volcanic sites.</p>
                            <hr />
                            <p>Created and administered by members of the Rosenstiel School of Marine and Atmospheric Science (RSMAS) Insarlab in Miami, Florida.</p>
                            <p>
                                <a className="btn btn-primary" href={"/volcanos/list"}>Volcanos List</a>
                                <a className="btn btn-primary" href={"/volcanos/map"}>Volcanos Map</a>
                            </p>
                        </Col>
                    </Row>
                 </Jumbotron>
            </Container>

        )
    }

}

export default HomeViewComponent