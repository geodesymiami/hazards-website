import React, {Component} from "react";
import TabPane from 'react-bootstrap/TabPane'
import axios from "axios";
import "./ImagesTabPane.css"

class ImagesTabPane extends Component{

    constructor(props){
        super(props)

        this.state = {
            image_type: this.props.image_type,
            satellites: ["S1A_DESC"],
            images: [
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg",
                        "https://images.catsolonline.com/cache/fo7x6dhiwqczswpoimve-500x500.jpg"
                    ]
        }
    }

    componentWillMount() {

        var id = this.props.haz_id

        axios.get(`http://0.0.0.0:5000/api/volcano/images/${id}`, {params: {image_types: this.state.image_type},mode: "cors"})
            .then((response) => {
                console.log(response)
            })

    }

    render(){

        return(

            <TabPane eventKey={this.state.image_type} className={"images"} style={{background: this.props.color}}>
                <div className={"row"}>
                    {this.state.satellites.map( (name, index) => {
                        return  <div>
                                    <h3>{name}</h3>
                                    {this.state.images.map( (name, index) => {
                                        return <img src={name} className={"image"}/>
                                    })}
                                </div>
                    })}
                </div>
            </TabPane>

        );
    }
}

export default ImagesTabPane;