import React, { Component } from 'react';
import Tabs from 'react-bootstrap/Tabs'
import Tab from 'react-bootstrap/Tab'
import ImagesTabPane from "./ImagesTabPane";
import Sidebar from "./Sidebar";
import Nav from "react-bootstrap/Nav";

class ImageTypeTabs extends Component {

  constructor(props) {
    super(props);

    this.state = {
      key: this.props.image_types[0]
    };

  }

  render() {

    return (
        <Tab.Container>
          <Nav variant={"tabs"} activeKey={this.state.key}>
            {
                this.props.image_types.map( (name, index) => {
                    name = name.toLowerCase().split(" ").join("_")
                    return  <Nav.Item>
                                <Nav.Link eventKey={name}>{name}</Nav.Link>
                            </Nav.Item>
                })
            }
          </Nav>
           <div className={'row'}>
              <div className={"col-lg-3"}>
                <Sidebar />
              </div>
              <div className={"col-lg-9"}>
                <Tab.Content>
                  {this.props.image_types.map( (name, index) => {
                        name = name.toLowerCase().split(" ").join("_")
                        return <ImagesTabPane image_type={name} key={name} haz_id={this.props.haz_id} images={this.props.images[name]}/>
                  })}
                </Tab.Content>
              </div>
            </div>

        </Tab.Container>
    );
  }
}

export default ImageTypeTabs;