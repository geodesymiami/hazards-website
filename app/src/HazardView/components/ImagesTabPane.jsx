import React, {Component} from "react";
import TabPane from 'react-bootstrap/TabPane'
import "./ImagesTabPane.css"

class ImagesTabPane extends Component{

    render(){

        var images_by_sat = this.props.images;

        var sats = Object.keys(images_by_sat)

        return(

            <TabPane eventKey={this.props.image_type} className={"images"}>
                <div className={"row"}>
                    {sats.map( (name, index) => {
                        return  <div className={"sat"} key={index}>
                                    <h3>{name}</h3>
                                    {images_by_sat[sats[index]].sort(
                                        function(a, b){
                                            return a.image_date > b.image_date;
                                        }).map(
                                            (name, index) => {
                                                return <img src={name["modified_image_url"]} className={"image"} alt={""} key={index}/>
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