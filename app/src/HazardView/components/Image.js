import React, { Component } from "react";
import { Button, Modal, ModalBody, ModalFooter } from 'react-bootstrap';

class Image extends Component{

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
            <div className={"image"}>
                <img src={this.props.url} className={"image"} alt={""} key={this.props.index} onClick={this.toggle} />
                <Modal show={this.state.modal} size={'lg'} onHide={this.toggle}>
                    <Modal.Header closeButton></Modal.Header>
                    <ModalBody>
                        <img src={this.props.url} alt={""} key={this.props.index} style={{width: "100%"}}/>
                    </ModalBody>
                </Modal>
            </div>

        )
    }

}

export default Image