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