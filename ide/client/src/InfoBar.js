import React from 'react';
import './InfoBar.css';
import { Play } from 'react-feather';

function InfoBar(props) {
  const {sendCode, clearConsole} = props;
  return (
    <div className="info-bar">
      <div className="buttons">
        <div className="run button" onClick={sendCode}>
          <p className="run-text text">run</p>
        </div>
        <div className="clear button" onClick={clearConsole}>
          <p className="clear-text text">clear</p>
        </div>
      </div>
    </div>
  );
}

export default InfoBar;