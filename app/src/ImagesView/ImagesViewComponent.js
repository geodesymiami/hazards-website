import React, {Component} from 'react'
import { Carousel, Modal, Container, Image } from 'react-bootstrap';

export default class ImagesViewComponent extends Component {
    constructor(...args) {
        super(...args)
        this.state = {modal: false, index: 0, direction: null}
    }
    render() {
        return <Container>
            <Carousel interval={null} 
            activeIndex={this.state.index} 
            direction={this.state.direction} 
            onSelect={(index, direction) => this.setState({index, direction})}
            >
                {
                    this.props.images.map((n, i) => (
                        <Carousel.Item 
                        key={i} 
                        onClick={() => this.setState({modal: true, url: n['full_image_url']})}
                        style={{cursor:'pointer'}}
                        >
                            <Image src={n['full_image_url']} fluid></Image>
                            <Carousel.Caption>
                                <h3>{n.date.substring(0, 2)}/{n.date.substring(2, 4)}/{n.date.substring(4, 8)}</h3>
                            </Carousel.Caption>
                        </Carousel.Item>
                    ))
                }
            </Carousel>
            <Modal show={this.state.modal} size="lg" centered onHide={() => this.setState({modal: false})}>
                <Modal.Body>
                    <Image src={this.state.url} fluid></Image>
                </Modal.Body>
            </Modal>
        </Container>
    }
}