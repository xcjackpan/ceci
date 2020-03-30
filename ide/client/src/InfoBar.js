import React from 'react';
import './InfoBar.css';
import { Play } from 'react-feather';

function InfoBar(props) {
  const {sendCode} = props;
  return (
    <div className="info-bar">
      <div className="run" onClick={sendCode}>
        <Play className="run-icon" />
      </div>
    </div>
  );
}

export default InfoBar;