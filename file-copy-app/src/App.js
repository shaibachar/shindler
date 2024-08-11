import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import GenerateJson from './GenerateJson';
import CopyFiles from './CopyFiles';
import ValidateFiles from './ValidateFiles';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <h1>File Management App</h1>
                <ul className="nav-tabs">
                    <li><Link to="/generate-json">Generate JSON</Link></li>
                    <li><Link to="/copy-files">Copy Files</Link></li>
                    <li><Link to="/validate-files">Validate Copy</Link></li>
                </ul>
                <div className="content">
                    <Routes>
                        <Route path="/generate-json" element={<GenerateJson />} />
                        <Route path="/copy-files" element={<CopyFiles />} />
                        <Route path="/validate-files" element={<ValidateFiles />} />
                        <Route path="/" element={<GenerateJson />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
