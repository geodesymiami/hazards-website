import React, { Component } from 'react';
import Tabs from 'react-bootstrap/Tabs'
import Tab from 'react-bootstrap/Tab'

class ImageTypeTabs extends Component {

  constructor(props) {
    super(props);

    this.state = {
      key: this.props.image_types[0]
    };

  }

  render() {

    return (
        <Tabs defaultActiveKey="profile" id="uncontrolled-tab-example" activeKey={this.state.key} onSelect={key => this.setState({ key })}>
            {this.props.image_types.map( (name, index) => {
                return <Tab eventKey={name} key={name} title={name}></Tab>
            })}
        </Tabs>
    );
  }
}

export default ImageTypeTabs;