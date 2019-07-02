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
      key: this.props.image_types[0],
      colors: ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    };

  }

  render() {

    return (
        <Tab.Container>
          <Nav variant={"tabs"} activeKey={this.state.key}>
            {this.props.image_types.map( (name, index) => {
                  return  <Nav.Item>
                            <Nav.Link eventKey={name}>{name}</Nav.Link>
                          </Nav.Item>
            })}
          </Nav>
          {/*<Tabs defaultActiveKey="profile" id="uncontrolled-tab-example" activeKey={this.state.key} onSelect={key => this.setState({ key })}>*/}
          {/*    {this.props.image_types.map( (name, index) => {*/}
          {/*        return <Tab eventKey={name} key={name} title={name}></Tab>*/}
          {/*    })}*/}
          {/*</Tabs>*/}
           <div className={'row'}>
              <div className={"col-lg-4"}>
                <Sidebar />
              </div>
              <div className={"col-lg-8"}>
                <Tab.Content>
                  {this.props.image_types.map( (name, index) => {
                    return <ImagesTabPane image_type={name} key={name} color={this.state.colors[index]}/>
                  })}
                </Tab.Content>
              </div>
            </div>

        </Tab.Container>
    );
  }
}

export default ImageTypeTabs;