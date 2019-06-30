import React, {Component} from "react";
import TabPane from 'react-bootstrap/TabPane'
import Sidebar from "./Sidebar";
import "./ImagesTabPane.css"

class ImagesTabPane extends Component{

    constructor(props){
        super(props)
    }

    render(){

        return(

            <TabPane eventKey={"test"}>
                <div className={"row"}>
                    <div className={"col-lg-4"}>
                        <Sidebar />
                    </div>
                    <div className={"col-lg-8"} style={{height: "100vh", background: "gray"}}></div>
                </div>
            </TabPane>

        );
    }
}

export default ImagesTabPane;