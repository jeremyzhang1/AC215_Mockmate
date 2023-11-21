import React, { useRef, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Editor from '@monaco-editor/react'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/App.css';

function MockmatePage() {
    const editorRef = useRef(null);
    const [editorText, setEditorText] = useState("# your code here")

    function handleEditorDidMount(editor, monaco) {
      editorRef.current = editor;
    }
  
    function showValue() {
      setEditorText(editorRef.current.getValue())
    }

    return (
        <Container>
            <h1>Mockmate Interview</h1>
            <Row>
                <Col>
                    <Button onClick={showValue}>Show value</Button>
                    <p>{editorText}</p>
                </Col>
                <Col>
                    <Editor height="90vh" defaultLanguage="python" defaultValue={editorText} theme="vs-dark" onMount={handleEditorDidMount}/>
                </Col>
            </Row>
        </Container>
    )
}

export default MockmatePage
