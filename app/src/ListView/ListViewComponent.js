import React, { Component } from 'react';
import './ListViewComponent.css';
import "font-awesome/css/font-awesome.min.css"
import {Link} from "@reach/router";


export default class ListViewComponent extends Component {

    constructor() {
        super();
        this.state = {
            volcanos: []
        }
    }

    componentDidMount() {
        console.log("component did mount");
        fetch("http://0.0.0.0:5000/api/volcano", {mode: 'cors'})
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                this.setState({volcanos: data.hazards},
                    () => console.log(this.state.volcanos))
            })
            .catch((error) => {
                console.log(error)
            })
    }

    render() {
        return (
            <div className="ListViewComponent">
                 <div className="">

                    

                    {/* Hard Coded List Card for example */}

                    <div className="container">
                        <h1>List View Component</h1>
                        <ul>
                            {this.state.volcanos.map(volcano =>

                            <li className="row">
                                <div className="hazard row">
                                    <div className={'col-lg-8'}>
                                        <h3>{volcano.name}</h3>
                                        <p>{volcano.location.latitude}, {volcano.location.longitude}</p>
                                    </div>
                                    <div className={'col-lg-2'}>
                                        <p>{volcano.last_updated}</p>
                                    </div>
                                    <div className={'col-lg-1'}>
                                        <h3>10</h3>
                                    </div>
                                    <div className={'col-lg-1'}>
                                        <Link to={`/hazard/${volcano.hazard_id}`}><i className="fa fa-chevron-right fa-lg"></i></Link>
                                    </div>
                                </div>
                            </li>
                            )}
                        </ul>
                    </div>
                    {/*<ul>*/}
                    {/*    <div className="row">*/}
                    {/*    {this.state.volcanoes.map(volcano => */}
                    {/*    <div className="col-4">*/}
                    {/*        <Card className="card-cont" style={{ width: '18rem' }}>*/}
                    {/*        <Card.Img variant='top' src={volcano.img} />*/}
                    {/*        <Card.Body>*/}
                    {/*            <Card.Title>{volcano.name}</Card.Title>*/}
                    {/*            <Card.Text>*/}
                    {/*            Location: {volcano.location},*/}
                    {/*            </Card.Text>*/}
                    {/*            <Card.Text>*/}
                    {/*            Elvation: {volcano.height}'*/}
                    {/*            </Card.Text>*/}
                    {/*        </Card.Body>*/}
                    {/*        </Card>*/}
                    {/*    </div>*/}
                    {/*    )}*/}
                    {/*    </div>*/}
                    {/*</ul>*/}
                </div>
            </div>
        )
    }
}