import React, { Component } from 'react';
import './ListViewComponent.css';
import "../font-awesome/css/font-awesome.min.css"
import {Container} from "react-bootstrap";
import axios from "axios";

var moment = require('moment')
const $ = require('jquery');
$.DataTable = require('datatables.net-bs4');

export default class ListViewComponent extends Component {

    constructor() {
        super();
        this.state = {
            volcanos: [],
            columns: [
                        {
                            title: 'ID',
                            data: 'hazard_id',
                        },
                        {
                            title: 'Name',
                            data: 'name',
                        },
                        {
                            title: 'Latitude',
                            data: 'latitude',
                        },
                        {
                            title: 'Longitude',
                            data: 'longitude',
                        },
                        {
                            title: 'Num Images',
                            data: 'num_images',
                        },
                        {
                            title: 'Last Updated',
                            data: 'last_updated',
                        }
                    ],
        }
    }

    componentDidMount() {
        console.log("Component did mount.")
        axios.get("http://129.114.17.74:5000/api/volcano", {mode: 'cors'})
            .then((response) => {
                this.setState({
                    volcanos: response.data.hazards
                })
            })
            .then( () => {
                console.log(this.state.volcanos)
                $("table").DataTable({
                    dom: "<'row'<'col-lg-6 left'l><'col-lg-6 right'f>><'data-table-wrapper't><'row'<'col-lg-12'p>>",
                    data: this.state.volcanos,
                    columns: this.state.columns,
                    ordering: true,
                    searching: true,
                    paging: true,
                    autoWidth: true,
                    columnDefs: [
                        {
                            "render": function (data, type, row) {
                                return `<a href='/volcanos/${row['hazard_id']}'>${data}</a>`;
                            },
                            "targets": 1
                        },
                        {
                            "render": function (data, type, row) {
                                return moment(data).format("YYYY-MM-DD").toString();
                            },
                            "targets": 5
                        },
                    ]
                })
            })
            .catch((error) => {
                console.log(error)
            })
    }

    componentWillUnmount(){
       $('.data-table-wrapper').find('table').DataTable().destroy(true);
    }

    shouldComponentUpdate() {
        return false;
    }

    render() {
        return (
            <Container>
                <h1 className={"page-title"}> Volcanos List </h1>
                <table className={"row-border"}/>
            </Container>
        )
    }
}