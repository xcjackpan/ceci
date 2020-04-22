import React from 'react';
import './InfoBar.css';

const simplePipeSample = 
`function addOne() {
  return pipe + 1;
}
print 5 into addOne();`

const chainPipeSample = 
`function double() {
  return pipe * 2;
}
print 2 into double() into double() into double() into double();`

const wackyPipeSample = 
`function printAndAdd() {
  print pipe;
  return pipe + 1;
}
loop(let i = 0; i < 3; i = i into printAndAdd();) {
  pass;
}`

const loopSample = 
`loop(let i = 0; i < 10; i = i + 1;) {
  print i; 
}

let i = 10;
loop(i >= 0;) {
  print i;
  i = i - 1;
}`

const functionSample = 
`function whichNumberIsGreater(a, b) {
  if (a > b) {
    print a;
  } elif (b > a) {
    print b;
  } else {
    print "They're equal.";
  }
}
whichNumberIsGreater(2,1);
whichNumberIsGreater(2,3);
whichNumberIsGreater(2,2);`

const fibonacciSample = 
`function fib(n) {
  let a = 0;
  let b = 1;
  let next = 0;
  loop(let i = 1; i < n; i = i + 1;) {
    next = a + b;
    a = b;
    b = next;
  }
  return b;
}
print fib(10);

function rfib(n) {
  if (n <= 1) {
    return n;
  }
  return fib(n-1) + fib(n-2);
}
print rfib(10);`

const codeSamples = [
  {
    name: "simple pipes",
    code: simplePipeSample,
  },
  {
    name: "chain pipes",
    code: chainPipeSample,
  },
  {
    name: "wacky pipes",
    code: wackyPipeSample,
  },
  {
    name: "loops",
    code: loopSample,
  },
  {
    name: "functions",
    code: functionSample,
  },
  {
    name: "fibonacci",
    code: fibonacciSample,
  },
]

function renderSample(sampleInfo, setCode) {
  return (
    <div className="sample button" onClick={() => {setCode(sampleInfo.code)}}>
      <p className="sample-text text">{sampleInfo.name}</p>
    </div>
  )
}

function InfoBar(props) {
  const {sendCode, setCode, clearConsole} = props;
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
      <div className="description">
        <p className="heading">This is Ceci.</p>
        <p className="text">
          Ceci's a programming language I made for fun. Here, you can
          play with some of Ceci's gimmicks and see it in action.
          <br/>
          <br/>
          To make this interpreter, I designed and created from scratch:
          <ul>
            <li>a CFG for the language</li>
            <li>a tokenizer</li>
            <li>an LL(1)/recursive-descent parser</li>
            <li>an evaluator</li>
          </ul>
          <br/>
          Here are some code samples as a jumping-off point:
        </p>
        <div className="samples">
          {
            codeSamples.map((elem) => {
              return renderSample(elem, setCode)
            })
          }
        </div>
        <p className="text">
          Few other things to note:
          <ul>
            <li>Ceci's still a WIP! There are no arrays/objects yet.</li>
            <li>Both "for" and "while" loops use the same keyword: "loop". They are differentiated by the expressions given</li>
            <li>You need a semicolon after the last expression in a "for" loop.</li>
          </ul>
          <br/>
          If you're interested in how I built Ceci, I kept a doc on everything
          I learned along the way. <a href="https://github.com/xcjackpan/ceci/blob/master/learnings.md">Take a look!</a>
        </p>
      </div>
    </div>
  );
}

export default InfoBar;