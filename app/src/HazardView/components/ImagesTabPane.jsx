import React, {Component} from "react";
import TabPane from 'react-bootstrap/TabPane'
import "./ImagesTabPane.css"
import Image from "./Image";

class ImagesTabPane extends Component{

    render(){

        var images_by_sat = this.props.images;

        var sats = Object.keys(images_by_sat)

        return(

            <TabPane eventKey={this.props.image_type} className={"images"}>
                <div className={"row"}>
                    {
                        sats.sort().map( (name, index) => {
                            return  <div className={"sat"} key={index}>
                                        <h3>{name}</h3>
                                        {
                                            images_by_sat[sats[index]].sort(
                                                function(a, b){
                                                    return a.image_date < b.image_date;
                                                }
                                            ).map(
                                                function(image, index){
                                                    return <Image url={image["modified_image_url"]} index={index} />
                                                }
                                            )
                                        }
                                    </div>
                        })
                    }
                </div>
            </TabPane>

        );
    }
}

export default ImagesTabPane;