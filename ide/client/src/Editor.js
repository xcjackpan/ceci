import React, { useEffect, useRef } from 'react';
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
    let pos = insert - 1;
    let indent = '';
    while (pos >= 0) {
      if (code[pos] === '\n') {
        break;
      } else if (code[pos] === tab) {
        indent += tab;
      } else {
        indent = '';
      }
      pos--;
    }
    updateCode([code.slice(0, insert), '\n', indent, code.slice(insert)].join(''));
    e.preventDefault();
    return insert + indent.length + 1;
  }
  return -1;
}

function Editor(props) {
  const {code, updateCode} = props;
  let inputRef = useRef(null);
  let outputRef = useRef(null)

  useEffect(() => {
    if (inputRef.current && shouldUpdateCursor) {
      inputRef.current.selectionEnd = cursor;
    }
  });
  useEffect(() => {
    outputRef.current.scrollTop = outputRef.current.scrollHeight
  }, [props.output]);

  return (
    <div className="editor">
      <textarea 
        name="input"
        ref={inputRef}
        onChange={(e) => {
          updateCode(e.target.value);
        }}
        onKeyDown={(e) => {
          cursor = handleKeyDown(e, code, updateCode);
          shouldUpdateCursor = (cursor !== -1)
        }}
        value={code}
      />
      <div className="output" ref={outputRef}>
        {props.output}
      </div>
    </div>
  );
}

export default Editor;