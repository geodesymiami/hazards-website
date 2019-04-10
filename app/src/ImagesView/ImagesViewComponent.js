import React, {Component} from 'react'
import { Carousel } from 'react-bootstrap';

export default class ImagesViewComponent extends Component {
    render() {
        return (
            <Carousel>
                {
                    this.props.images.map(n => (
                        <Carousel.Item>
                            <img src={n['full_image_url']}></img>
                            <Carousel.Caption>
                                <h3>{n.date.substring(0, 2)}/{n.date.substring(2, 4)}/{n.date.substring(4, 8)}</h3>
                            </Carousel.Caption>
                        </Carousel.Item>
                    ))
                }
            </Carousel>
        )
    }
}