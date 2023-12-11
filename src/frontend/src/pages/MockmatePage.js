import React, { useRef, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Editor from '@monaco-editor/react'
import Markdown from 'react-markdown'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/App.css';

function MockmatePage() {
    const baseUrl = "http://localhost:9000"
    const defaultQuestion = ""
    // const defaultHelpText = "Click the button to get a hint"
    // const defaultFeedbackText = "Click the button to submit and get feedback"
    const editorRef = useRef(null);
    const [editorText, setEditorText] = useState("# your code here")
    const [question, setQuestion] = useState(defaultQuestion)
    const [solution, setSolution] = useState("")
    const [explaination, setExplaination] = useState("")
    const [helpText, setHelpText] = useState("")

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
    }

    function getEditorValue() {
        setEditorText(editorRef.current.getValue())
    }

    function generateQuestion() {
        fetch(baseUrl + '/get-interview-question/?' + new URLSearchParams({
            difficulty: 'Easy',
        }))
            .then(response => response.json())
            .then(data => { setQuestion(data.body) })
            .catch(error => console.error(error));
    }

    function getSolution() {
        fetch(baseUrl + "/get-question-solution")
            .then(response => response.json())
            .then(data => { setSolution(data.body) })
            .catch(error => console.error(error));
    }

    function getExplaination() {
        fetch(baseUrl + "/get-question-explanation")
            .then(response => response.json())
            .then(data => { setExplaination(data.body) })
            .catch(error => console.error(error));
    }

    function getHelp() {
        fetch(baseUrl + '/query-chat?' + new URLSearchParams({
            query: editorText
        }))
            .then(response => response.json())
            // .then(data => { setHelpText([...helpText, data.body]) }) 
            .then(data => { setHelpText(data.body) })
            .catch(error => console.error(error));
    }

    return (
        <Container>
            <h1>Mockmate Interview</h1>
            <Row>
                <Col>
                    <h3>Question:</h3>
                    {question === defaultQuestion ? <Button variant='dark' onClick={generateQuestion}>Start Interview</Button> : <Markdown children={question} />}
                    <br></br>
                    <h3>Help:</h3>
                    <Button variant='dark' onClick={getHelp}>Get Hint</Button>
                    <Markdown>{helpText}</Markdown>
                    <h3>Solution and Explanation:</h3>
                    <Button variant='dark' onClick={getSolution} style={{ marginRight: "8px" }}>Show Solution</Button>
                    <Markdown children={solution} />
                    <Button variant='dark' onClick={getExplaination}>Show Explanation</Button>
                    <Markdown children={explaination} />
                </Col>
                <Col>
                    <Editor height="90vh" defaultLanguage="python" defaultValue={editorText} theme="vs-dark" onMount={handleEditorDidMount} onChange={getEditorValue}/>
                </Col>
            </Row>
        </Container>
    )
}

export default MockmatePage
