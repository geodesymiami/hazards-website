import React, { Component } from 'react';
import { Card } from 'react-bootstrap';
import './ListViewComponent.css';


export default class ListViewComponent extends Component {

    constructor() {
        super();
        this.state = {
            volcanoes: []
        }
    }

    componentDidMount() {
        fetch('/api/Volcanoes')
        .then(res => res.json())
        .then(volcanoes => this.setState({volcanoes}, 
            () => console.log('volcanoes', volcanoes)
            ));

       return null;
    }

    render() {
        return (
            <div className="ListViewComponent">
                 <div className="">

                    

                    {/* Hard Coded List Card for example */}
                    <div className="container">
                    <h1>List View Component</h1>
                        <div className="row">
                            <div className="col-md-4">
                                <Card className="card-cont" style={{ width: '18rem' }}>
                                    <Card.Img variant='top' 
                                    src="https://s.newsweek.com/sites/www.newsweek.com/files/styles/embed_tablet/public/2017/12/19/image-512766800.jpg" />
                                    <Card.Body>
                                        <Card.Title>Volcano Name: Kilahuea</Card.Title>
                                        <Card.Text>
                                            Location: Hawai
                                        </Card.Text>
                                        <Card.Text>
                                            Elevation: 5000'
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </div>
                            <div className="col-md-4">
                                <Card className="card-cont" style={{ width: '18rem' }}>
                                    <Card.Img variant='top'
                                        src="https://s.newsweek.com/sites/www.newsweek.com/files/styles/embed_tablet/public/2017/12/19/image-512766800.jpg" />
                                    <Card.Body>
                                        <Card.Title>Volcano Name: Kilahuea</Card.Title>
                                        <Card.Text>
                                            Location: Hawai
                                        </Card.Text>
                                        <Card.Text>
                                            Elevation: 5000'
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </div>
                            <div className="col-md-4">
                                <Card className="card-cont" style={{ width: '18rem' }}>
                                    <Card.Img variant='top'
                                        src="https://s.newsweek.com/sites/www.newsweek.com/files/styles/embed_tablet/public/2017/12/19/image-512766800.jpg" />
                                    <Card.Body>
                                        <Card.Title>Volcano Name: Kilahuea</Card.Title>
                                        <Card.Text>
                                            Location: Hawai
                                        </Card.Text>
                                        <Card.Text>
                                            Elevation: 5000'
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </div>
                        </div>
                    </div>
                    <ul>
                        <div className="row">
                        {this.state.volcanoes.map(volcano => 
                        <div className="col-4">
                            <Card className="card-cont" style={{ width: '18rem' }}>
                            <Card.Img variant='top' src={volcano.img} />
                            <Card.Body>
                                <Card.Title>{volcano.name}</Card.Title>
                                <Card.Text>
                                Location: {volcano.location},
                                </Card.Text>
                                <Card.Text>
                                Elvation: {volcano.height}'
                                </Card.Text>
                            </Card.Body>
                            </Card>
                        </div>
                        )}
                        </div>
                    </ul>
                </div>
            </div>
        )
    }
}