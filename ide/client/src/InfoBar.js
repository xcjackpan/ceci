import React from 'react';
import './InfoBar.css';

const simplePipeSample = 
`function addOne() {
\treturn pipe + 1;
}
print 5 into addOne();`

const chainPipeSample = 
`function double() {
\treturn pipe * 2;
}
print 2 into double() into double() into double() into double();`

const wackyPipeSample = 
`function printAndAdd() {
\tprint pipe;
\treturn pipe + 1;
}
loop(let i = 0; i < 3; i = i into printAndAdd();) {
\tpass;
}`

const loopSample = 
`loop(let i = 0; i < 10; i = i + 1;) {
\tprint i; 
}

let j = 10;
loop(j >= 0) {
\tprint j;
\tj = j - 1;
}`

const functionSample = 
`function whichNumberIsGreater(a, b) {
\tif (a > b) {
\t\tprint a;
\t} elif (b > a) {
\t\tprint b;
\t} else {
\t\tprint "They're equal.";
\t}
}
whichNumberIsGreater(2,1);
whichNumberIsGreater(2,3);
whichNumberIsGreater(2,2);`

const fibonacciSample = 
`function fib(n) {
\tlet a = 0;
\tlet b = 1;
\tlet next = 0;
\tloop(let i = 1; i < n; i = i + 1;) {
\t\tnext = a + b;
\t\ta = b;
\t\tb = next;
\t}
\treturn b;
}
print fib(10);

function rfib(n) {
\tif (n <= 1) {
\t\treturn n;
\t}
\treturn fib(n-1) + fib(n-2);
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
        <p className="text">
          Ceci's a programming language I made for fun. This is a quick and dirty web app
          running the Ceci interpreter.
        </p>
        <p className="heading">Piping</p>
        <p className="text">
          Ceci's gimmick. Any expression can be piped into a function using the keyword <span className="code">into</span>.
          That expression is accessible from within the function as the variable <span className="code">pipe</span>.
        </p>
        <p className="heading">Syntax</p>
        <p className="text">
          <i>Loops</i>: For/while loops both use the keyword <span className="code">loop</span>, differentiated by the expressions passed in. You'll need a
          semicolon after the last expression in a for-loop.
          <br/>
          <br/>
          <i>If-statements</i>: Uses keywords <span className="code">if</span>, <span className="code">elif</span>, and <span className="code">else</span>.
          <br/>
          <br/>
          <i>Variables</i>: No static types. Declared with <span className="code">let</span>.
          <br/>
          <br/>
          <i>Functions</i>: Declared with <span className="code">function</span>. Called using brackets.
          <br/>
          <br/>
          <i>Scoping</i>: Functions have their own scope. Loops and if-statements do not.
          <br/>
          <br/>
          <i>Printing</i>: Uses keyword <span className="code">print</span>. Curly brackets not needed.
          <br/>
          <br/>
          <i>Other syntax</i>: Use curly-braces to enclose blocks and semicolons to end lines.
        </p>
        <p className="heading">Code Samples</p>
        <div className="samples">
          {
            codeSamples.map((elem) => {
              return renderSample(elem, setCode)
            })
          }
        </div>
        <p className="heading">More info</p>
        <p className="text">
          <a href="https://github.com/xcjackpan/ceci/">Source code</a>
          <br/>
          <br/>
          <a href="https://github.com/xcjackpan/ceci/blob/master/learnings.md">What I learned building Ceci</a>
        </p>
      </div>
    </div>
  );
}

export default InfoBar;