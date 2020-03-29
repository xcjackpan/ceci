import React, { useState } from 'react';
import './Editor.css';

function handleKeyDown(e, code, updateCode) {
  const tab = '\t'
  if (e.key === 'Tab' && !e.shiftKey) {
    e.preventDefault();
    updateCode(code + tab)
  } else if  (e.key === 'Enter') {
    let insert = e.target.selectionEnd;
    let pos = insert;
    let indent = '';
    while (pos >= 0) {
      if (code[pos] === '\n') {
        break;
      } else if (code[pos] === '\t') {
        indent += '\t';
      } else {
        indent = '';
      }
      pos--;
    }
    updateCode([code.slice(0, insert), '\n', indent, code.slice(insert)].join(''));
    e.preventDefault();
  }
}

function Editor() {
  const [code, updateCode] = useState("");
  return (
    <div className="editor">
      <textarea 
        name="input"
        onChange={(e) => {
          updateCode(e.target.value)
        }}
        onKeyDown={(e) => handleKeyDown(e, code, updateCode)}
        value={code}
      />
    </div>
  );
}

export default Editor;