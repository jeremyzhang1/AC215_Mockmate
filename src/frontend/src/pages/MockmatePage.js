import React from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Editor from '@monaco-editor/react'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/App.css';

function MockmatePage() {
    return (
        <Container>
            <h1>Mockmate Interview</h1>
            <Row>
                <Col>
                    <p>Interview transcript</p>
                </Col>
                <Col>
                    <Editor height="90vh" defaultLanguage="python" defaultValue="# your code here" theme="vs-dark"/>
                </Col>
            </Row>
        </Container>
    )
}

export default MockmatePage
