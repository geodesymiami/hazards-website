import React, { Component } from 'react';
import './MapViewComponent.css';
import {  Map, Marker, Popup } from 'react-leaflet';
import ReactDOM from 'react-dom';

export default class MapViewComponent extends Component {
    constructor(){
	super()
	this.state = {
	    lat: 25.5,
	    lng: -80.5,
	    zoom: 2
	}
    }

    render() {
	
        const position = [this.state.lat, this.state.lng];
	return (
            <div className="MapViewComponent">
	    <h1>Map View</h1>
      	    <Map center = {position} zoom = {this.state.zoom}>
	    <Marker position = {position}>
	    <Popup>Popup 
	    <br/> More information... 
	    </Popup>
	    </Marker>
	    </Map>
	       
            </div>
		);
    }
}

ReactDOM.render(<MapViewComponent />, document.getElementById('root'))
