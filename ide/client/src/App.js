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
      updateOutput(output + "> " + response.data.output + "\n")
    })
  }

  function clearConsole() {
    updateOutput("");
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
      /> 
    </div>
  );
}

export default App;
