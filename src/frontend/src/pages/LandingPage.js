import React from "react";
import Button from 'react-bootstrap/Button'
import {Link} from 'react-router-dom'
import '../styles/App.css'
import 'bootstrap/dist/css/bootstrap.min.css';

require('dotenv').config()

function App() {

  return (
    <div className="home">
      <div>
        <h1 className="text-center" style={{ fontSize: "4em", color: "white", paddingTop: "10%" }}><strong>Mockmate</strong></h1>
        <br />
        <p className="text-center" style={{ fontSize: "1.4em", color: "white" }}>AI-powered technical interview practice.</p>
        <br />

        <div className="text-center">
          <Button variant='light' className='log-in-button'>
            <Link to="/app" className='no-style-link'>Get Started</Link>
          </Button>
        </div>
      </div>

    </div>
  )
}

export default App;
