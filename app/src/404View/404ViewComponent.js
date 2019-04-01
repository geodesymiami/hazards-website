import React, {Component} from 'react'
import { Jumbotron, Button } from 'react-bootstrap';
import { Link } from '@reach/router';

export default class FourOhFourViewComponent extends Component {
    render() {
        return (
            <Jumbotron>
                <h1>404: Page Not Found</h1>
                <p>
                    Sorry, looks like the page you were trying to get to does not exist.
                </p>
                <Button as={Link} to="/" href="/">Go Home</Button>
            </Jumbotron>
        )
    }
}