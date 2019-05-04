import React, { Component } from 'react'
import {  Map, Marker, TileLayer, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
	iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
	    iconUrl: require('leaflet/dist/images/marker-icon.png'),
	    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
	    })
 
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
	    zoom: 3
	}
	}

    render() {
	
        const position = [this.state.lat, this.state.lng];
	return (
	    <div className='MapViewComponent'>
       	    <Map center = {position} zoom = {this.state.zoom} style={{width:'100%', height:'600px'}}>
	    <TileLayer
	    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
	    attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
	    />
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
