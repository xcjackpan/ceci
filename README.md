*If you're interested in some of the problems I faced in building Ceci and how I solved them, check out `learnings.md`*

***

**Ceci** is a programming language I designed for fun. This is an interpreter for Ceci built in Python (double-interpretedness, I know). It's composed of:
  - a tokenizer
  - a CFG I built from scratch
  - an LL(1)/recursive-descent parser
  - an evaluator

***

### Ceci's Gimmick
Ceci's gimmick (and [namesake](https://en.wikipedia.org/wiki/The_Treachery_of_Images)) is the concept of **piping**. 
With piping, whatever value you send `into` a function is accessible within that function as the `pipe` variable:
```
  function addOne() {
    return pipe + 1;
  }
  print 5 into addOne();
```
```
  6
```
You can chain pipes:
```
  function double() {
    return pipe * 2;
  }
  print 2 into double() into double() into double() into double();
```
```
  32
```
And you can even do wackier stuff:
```
  function printAndAdd() {
    print pipe;
    return pipe + 1;
  }
  loop(let i = 0; i < 3; i = i into printAndAdd();) {
    pass;
  }
```
```
  0
  1
  2
```

***

### Other Stuff
Ceci also does other normal programming language things. There's math:
```
  print 1 - (1 + 1) * (2 ^ 2);
```
```
  -7
```

We can do if-statements and regular functions:
```
  function whichNumberIsGreater(a, b) {
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
  whichNumberIsGreater(2,2);
```
```
  2
  3
  They're equal.
```

There's also variables and loops (except for/while both use the same keyword and are differentiated by the number of expressions passed in):
```
  let a = 0;
  loop (a < 3) {
    a = a + 1;
    print a;
  }
  print "======";
  loop (let i = 0; i < 3; i = i + 1;) {
    print i;
  }
```
```
  0
  1
  2
  ======
  0
  1
  2
```

Here's a classic Fibonacci function taken straight from a unit test:
```
  function fib(n) {
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
```
```
  55
```

And here's a recursive version of Fibonacci if you're into that:
```
  function fib(n) {
    if (n <= 1) {
      return n;
    }
    return fib(n-1) + fib(n-2);
  }
  print fib(10);
```
```
  55
```

### Wanna try it yourself?
Here are your options:
* Clone the repo and run the interpreter directly
  * To run unittests: `python -m unitttest`
  * To run shell-mode: `python -m unnamed.unnamed`
  * To run an input program: `python -m unnamed.unnamed < {FILE_NAME_OF_INPUT_PROGRAM}`

* There'll be a web environment soon -- WIP
