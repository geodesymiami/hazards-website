import React, {Component} from "react";
import TabPane from 'react-bootstrap/TabPane'
import "./ImagesTabPane.css"

class ImagesTabPane extends Component{

    constructor(props){
        super(props)
    }

    render(){

        return(

            <TabPane eventKey={this.props.image_type} className={"images"} style={{background: this.props.color}}>
                <div className={"row"}>

                </div>
            </TabPane>

        );
    }
}

export default ImagesTabPane;