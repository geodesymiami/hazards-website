import React, { Component } from 'react';
import Tab from 'react-bootstrap/Tab'
import ImagesTabPane from "./ImagesTabPane";
import Sidebar from "./Sidebar";
import Nav from "react-bootstrap/Nav";

class ImageTypeTabs extends Component {

  constructor(props) {
    super(props);

    this.state = {
      key: ""
    };

  }

  componentWillReceiveProps(nextProps, nextContext) {
      this.setState({
          key: nextProps.image_types[0]
      })
  }

    render() {
        console.log(this.state.key)
        console.log(this.props.filter_func)
        return (
            <Tab.Container activeKey={this.state.key}>
              <Nav variant={"tabs"} onSelect={key => this.setState({ key })}>
                {
                    this.props.image_types.map( (name, index) => {
                        var formatted_name = name.split("_").map(w => w.charAt(0).toUpperCase() + w.substring(1)).join(" ")
                        return  <Nav.Item key={name}>
                                    <Nav.Link eventKey={name} key={name}>{formatted_name}</Nav.Link>
                                </Nav.Item>
                    })
                }
              </Nav>
               <div className={'row'}>
                  <div className={"col-lg-3"}>
                    <Sidebar haz_id={this.props.haz_id} filter_func={this.props.filter_func}/>
                  </div>
                  <div className={"col-lg-9"}>
                    <Tab.Content>
                      {this.props.image_types.map( (name, index) => {
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