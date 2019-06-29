import React, { Component } from 'react';
import './ListViewComponent.css';
import "font-awesome/css/font-awesome.min.css"
import { MDBDataTable } from 'mdbreact';
import {Container} from "react-bootstrap";


export default class ListViewComponent extends Component {

    constructor() {
        super();
        this.state = {
            volcanos: [],
            data: {}
        }
    }

    componentDidMount() {
        console.log("component did mount");
        fetch("http://0.0.0.0:5000/api/volcano", {mode: 'cors'})
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                this.setState({volcanos: data.hazards},() =>
                console.log(this.state.volcanos))
                var tabledata = {
                    columns: [
                        {
                            label: 'ID',
                            field: 'hazard_id',
                            sort: 'asc'
                        },
                        {
                            label: 'Name',
                            field: 'name',
                            sort: 'asc'
                        },
                        {
                            label: 'Latitude',
                            field: 'latitude',
                            sort: 'asc'
                        },
                        {
                            label: 'Longitude',
                            field: 'longitude',
                            sort: 'asc'
                        },
                        {
                            label: 'Num Images',
                            field: 'num_images',
                            sort: 'asc'
                        },
                        {
                            label: 'Last Updated',
                            field: 'last_updated',
                            sort: 'asc'
                        },
                    ],
                    rows: this.state.volcanos
                };

                this.setState({data: tabledata})
            })
            .catch((error) => {
                console.log(error)
            })
    }

    render() {
        return (
            <Container>
                <h1 className={"page-title"}> Volcanos List </h1>
                <MDBDataTable data={this.state.data} sortable/>
            </Container>
        )
    }
}