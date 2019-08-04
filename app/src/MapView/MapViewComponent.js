import React, { Component } from 'react'
import {  Map, Marker, TileLayer, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet';
import './MapViewComponent.css'
import axios from "axios";

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
			 markers: []
		 }
	}

	componentWillMount() {

      axios.get(`http://0.0.0.0:5000/api/volcano`, {mode: 'cors'})
            .then( (response) => {
                this.setState({
					markers: response['data']['hazards']
				})
            })


	}
    render() {
       
		return (
			<div className='MapViewComponent'>
				<Map center = {[0, 0]} zoom = {3} style={{width: '100vw', height: '100vh'}}>
					<TileLayer
						url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
						attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
					/>
					{
						this.state.markers.map((hazard, idx) => {
							const position = [hazard['latitude'], hazard['longitude']]
							return <Marker key={`marker-${idx}`} position={position}>
										<Popup>
											<h6>{hazard['name']}</h6>
											<p><b>Hazard ID:</b> {hazard['hazard_id']}</p>
											<p><b>Number of images:</b> {hazard['num_images']}</p>
											<p><b>Most Recent Image:</b> {hazard['last_updated']}</p>
											<a className={'btn btn-md brn-primary'} href={`/volcanos/${hazard['hazard_id']}`}>See Details</a>
										</Popup>
									</Marker>
						})
					}
				</Map>

			</div>
		)
    }
 }
