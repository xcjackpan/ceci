import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Editor from './Editor';
import InfoBar from './InfoBar';

function App() {
  const [code, updateCode] = useState("");
  const [output, updateOutput] = useState([]);

  function sendCode(code) {
    axios.post('http://localhost:5000/run-code', {
      program: code,
    })
    .then(function (response) {
      let message = "Something went wrong! Try again in a moment."
      if (response.data.error) {
        message = response.data.error
      } else if (response.data.output) {
        message = response.data.error
      }
      updateOutput(output + "> " + message + "\n")
    })
  }

  function clearConsole() {
    updateOutput("");
  }

  function setCode(code) {
    updateCode(code)
  }

  return (
    <div className="App">
      <Editor
        code={code} 
        updateCode={updateCode}
        output={output}
      />
      <InfoBar 
        sendCode={() => sendCode(code)}
        clearConsole={clearConsole}
        setCode={setCode}
      /> 
    </div>
  );
}

export default App;
