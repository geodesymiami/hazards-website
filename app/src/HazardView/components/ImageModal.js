//ModalComponent.js
import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class ImageModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {modal: false};

        this.toggle = this.toggle.bind(this);

    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
    }



    render() {
        return (

            <Modal isOpen={this.state.modal}>
              <ModalHeader>IPL 2018</ModalHeader>
              <ModalBody>
                  <h1>Test</h1>
              </ModalBody>
              <ModalFooter>
                <input type="submit" value="Submit" color="primary" className="btn btn-primary" />
                <Button color="danger" onClick={this.toggle}>Cancel</Button>
              </ModalFooter>
            </Modal>

        );
    }
}

export default ImageModal