import React, { Component } from 'react';
import Tab from 'react-bootstrap/Tab'
import ImagesTabPane from "./ImagesTabPane";
import Sidebar from "./Sidebar";
import Nav from "react-bootstrap/Nav";

class ImageTypeTabs extends Component {

  constructor(props) {
    super(props);

    // Set appropriate key here
    this.state = {
        key: "",
        url_params: {}
    };

  }

  componentWillReceiveProps(nextProps, nextContext) {
      var active_key = nextProps.image_types.includes(this.props.active_image_type) ? this.props.active_image_type : nextProps.image_types[0]
      this.setState({
          key: active_key,
          url_params: nextProps.url_data
      })
  }

    render() {
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
                    <Sidebar
                        haz_id={this.props.haz_id}
                        url_data={this.state.url_params}
                        filter_func={this.props.filter_func}
                    />
                  </div>
                  <div className={"col-lg-9"}>
                    <Tab.Content>
                      {this.props.image_types.map( (name, index) => {
                            return <ImagesTabPane
                                        image_type={name}
                                        key={name}
                                        haz_id={this.props.haz_id}
                                        images={this.props.images[name]}
                                    />
                      })}
                    </Tab.Content>
                  </div>
                </div>

            </Tab.Container>
        );
  }
}

export default ImageTypeTabs;