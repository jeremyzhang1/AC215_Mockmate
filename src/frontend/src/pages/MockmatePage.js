import React, { useRef, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Editor from '@monaco-editor/react'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/App.css';

function MockmatePage() {
    const baseUrl = "http://127.0.0.1:8000" // TODO: Replace with actual production address
    const defaultQuestion = ""
    const defaultHelpText = "Click the button to get a hint"
    const defaultFeedbackText = "Click the button to submit and get feedback"
    const editorRef = useRef(null);
    const [editorText, setEditorText] = useState("# your code here")
    const [question, setQuestion] = useState(defaultQuestion)
    const [helpText, setHelpText] = useState(defaultHelpText)
    const [feedbackText, setFeedbackText] = useState(defaultFeedbackText)

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
    }

    function showValue() {
        setEditorText(editorRef.current.getValue())
        console.log(editorText)
    }

    function generateQuestion() {
        fetch(baseUrl + '/get-interview-question')
            .then(response => response.json())
            .then(data => {setQuestion(data.Question)})
            .catch(error => console.error(error));
    }

    function getHelp() {

    }

    function getFeedback() {

    }

    return (
        <Container>
            <h1>Mockmate Interview</h1>
            <Row>
                <Col>
                    <h3>Question:</h3>
                    {question == defaultQuestion ? <Button variant='dark' onClick={generateQuestion}>Start Interview</Button> : question}
                    <br></br>
                    <h3>Help:</h3>
                    <Button variant='dark' onClick={getHelp}>Hint</Button>
                    <p>{helpText}</p>
                    <h3>Feedback:</h3>
                    <Button variant='dark' onClick={getFeedback}>Submit</Button>
                    <p>{feedbackText}</p>
                    <Button variant='dark' onClick={showValue}>Show value</Button>
                    <p>{editorText}</p>
                </Col>
                <Col>
                    <Editor height="90vh" defaultLanguage="python" defaultValue={editorText} theme="vs-dark" onMount={handleEditorDidMount} />
                </Col>
            </Row>
        </Container>
    )
}

export default MockmatePage
