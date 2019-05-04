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

export default class MapViewComponent extends Component {
	constructor(){
	 super()
	 this.state = {
	     markers: [[51.5, -0.09], [52,-0.5]]
	}
	}
    addMarker = (e) => {
	const {markers} = this.state
	markers.push(e.latlng)
	this.setState({markers})
    }

    render() {
       
	return (
	    <div className='MapViewComponent'>
       	    <Map center = {[51.505, -0.09]} zoom = {3} style={{width:'100%', height:'600px'}}>
	    <TileLayer
	    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
	    attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
	    />
		{this.state.markers.map((position, idx) =>
					<Marker key={`marker-${idx}`} position = {position}>
	    <Popup>Popup 
	    <br/> More information... 
	    </Popup>
	    </Marker>)}
	    </Map>
	       
	    </div>
		)
    }
 }
