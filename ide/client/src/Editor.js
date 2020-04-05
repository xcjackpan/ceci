import React, { useEffect } from 'react';
import './Editor.css';

let cursor = 0;
let shouldUpdateCursor = false;

function handleKeyDown(e, code, updateCode) {
  const tab = '\t'
  if (e.key === 'Tab' && !e.shiftKey) {
    let insert = e.target.selectionEnd;
    updateCode([code.slice(0, insert), tab, code.slice(insert)].join(''));
    e.preventDefault();
    return insert + 1;
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
    return insert + 1;
  }
  return -1;
}

function Editor(props) {
  const {code, updateCode} = props;
  let inputRef = null;

  useEffect(() => {
    if (inputRef && shouldUpdateCursor) {
      inputRef.selectionEnd = cursor;
    }
  });

  return (
    <div className="editor">
      <textarea 
        name="input"
        ref={(textarea) => {inputRef = textarea}}
        onChange={(e) => {
          updateCode(e.target.value);
        }}
        onKeyDown={(e) => {
          cursor = handleKeyDown(e, code, updateCode);
          shouldUpdateCursor = (cursor !== -1)
        }}
        value={code}
      />
      <div className="output">
        {props.output}
      </div>
    </div>
  );
}

export default Editor;