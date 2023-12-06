import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import MockmatePage from './pages/MockmatePage';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/App.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/app" element={
                    <MockmatePage />
                } />
                <Route path="/" element={
                    <LandingPage />
                } />
            </Routes>
        </Router>
    )
}

export default App;
