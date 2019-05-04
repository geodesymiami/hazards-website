import React, { Component } from 'react'
import './MapViewComponent.css'
import {  Map, Marker, TileLayer, Popup } from 'react-leaflet'
 
    type State ={
    lat: number,
    lng: number,
    zoom: number,
}
    export default class MapViewComponent extends Component<{},State> {
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
            <div className='MapViewComponent'>
	    <h1>Map View</h1>
      	    <Map center = {position} zoom = {this.state.zoom}>
	    <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
	    <Marker position = {position}>
	    <Popup>Popup 
	    <br/> More information... 
	    </Popup>
	    </Marker>
	    </Map>
	       
        </div>
		)
    }
 }
