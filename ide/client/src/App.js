import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Editor from './Editor';
import InfoBar from './InfoBar';

function sendCode(code) {
  axios.post('/run-code', {
    program: code,
  })
  .then(function (response) {
    console.log(response)
  })
}

function App() {
  const [code, updateCode] = useState("");
  return (
    <div className="App">
      <Editor code={code} updateCode={updateCode}/>
      <InfoBar sendCode={() => sendCode(code)} /> 
    </div>
  );
}

export default App;
