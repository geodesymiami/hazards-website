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

    }

    render(){

        var images_by_sat = this.props.images;

        //images_by_sat.map( (name, index) => { console.log(name); return name})

        var sats = Object.keys(images_by_sat)

        console.log(sats)
        console.log(images_by_sat[sats[0]])

        return(

            <TabPane eventKey={this.props.image_type} className={"images"}>
                <div className={"row"}>
                    {sats.map( (name, index) => {
                        return  <div className={"sat"}>
                                    <h3>{name}</h3>
                                    {images_by_sat[sats[index]].sort(
                                        function(a, b){
                                            return a.image_date > b.image_date;
                                        }).map(
                                            (name, index) => {
                                                console.log(name["modified_image_url"])
                                                return <img src={name["modified_image_url"]} className={"image"}/>
                                            }
                                        )
                                }
                                </div>
                    })}
                </div>
            </TabPane>

        );
    }
}

export default ImagesTabPane;