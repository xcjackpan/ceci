These are some notes I'm keeping for stuff I learn along the way.

(This is mostly a learning exercise/for fun so pardon my use of an interpreted language to build
another interpreted language.)

## Order of operations
The terminals that are "deeper" down a parse tree are evaluated first. By having higher-precedence operations
be derived from more rules, our grammar can naturally the mathematical order of operations.

eg. In `expr -> expr +|- factor`, `factor -> factor *|/ term`, any node representing multiplication or 
division are further down the tree and so are evaluated first.

***

## PROBLEM: Top-down parsers and left/right-recursiveness
*Note: A left-recursive grammar is one with rules like `A -> AB`, note how the recursive term `A` occurs on the left of the RHS. A right-recursive grammar is one with rules like `A -> BA`.*

A top-down parser (eg. the one I'm building) will recurses itself to death when trying to 
parse a left-recursive grammar. That's because with a production like `A -> AB`, we'd try to parse the `A` first, which means we'd just use the rule `A -> AB` again. Ideally, we'd want a right-recursive grammar with rules like `A -> BA` so that we would parse `B` using some other rule. You can see this left-recursive grammar in `cfg-v1.txt`. 

But if I use a right-recursive grammar, then everything becomes right-associative. For example, `3 - 6 + 8` gets parsed as `3 - (6 + 8)`. This happens because with rules like `expr -> factor PLUS expr`, the result of parsing the `expr` on the right-hand-side
would be "deeper" down the parse tree than the result of parsing `factor`. This means the `expr` gets evaluated first, resulting
in right-associativity. 

### SOLUTION: Factoring grammars
My solution to the above problem was to factor my grammar so that it is no longer left-recursive. Compare 
`cfg-v1.txt` with `cfg-v2.txt`.

eg. Replace every derivation `A -> AB` with `A -> Ba, a -> Ba`

The downside of this is that my parse tree gets much larger, but the upside is that it's better trashing
my current top-down parser for a bottom-up one.

***

## PROBLEM: Mathematical expressions, boolean tests, and prefixes
A prefix-free language is one where no word is a prefix of another. For example, `{a, ab}` is **not** 
prefix-free. I designed my grammar to be prefix-free because that makes it easy to parse - once you
see the first token, you know what rule should be used without needing a lookahead.

But in `cfg-v2.txt`, you can see that I didn't account for something: mathematical expressions are a prefix
of boolean tests. You can see how `3 + 5` is a prefix of `3 + 5 < 7`. This means that when our parser sees the 
tokens `3 + 5`, we don't know whether to create a node for `expr` or `test`.

### SOLUTION: Revising my grammar
The problem was that since I had `test` and `expr` as totally unrelated ParseNodes, there was no way to 
figure out if I was reading in an `expr` or part of a `test`. To solve, this I modified my grammar once more:
`cfg-v3.txt`. I added a "layer" of nonterminals above my `expr` which could derive boolean tests. This works well
for two reasons:
  - Since now `test` and `expr` can be derived from the same "chain" of productions, it doesn't matter that our grammar
    isn't prefix free -- there's only one rule to use.
  - Order of operations is preserved. When you see `3 + 5 < 10`, the `<` gets evaluated last. By placing the layer
    of nonterminals *above* `expr`, we ensure that order of operations is respected.

***

## PROBLEM: Ambiguous grammars
An ambiguous grammar is one where the same result can be achieved by either two different left-derivations or two 
different right-derivations. In other words, there are at least two nontrivially distinct ways to derive the same string.
For example, `A -> aa, A -> AA, A -> a` is an *ambiguous* grammar since the string `aa` can be derived in 
two nontrivially distinct ways.

For obvious reasons, I tried really hard to make sure my grammar was unambiguous when I designed my language. This worked
well for the most part, but I had overlooked a key detail which I only realized when working with functions.
Consider the input `1 + a(12)`. I use whitespace as a delimiter and to make my life while tokenizing easier, I preprocessed by inserting spaces between every token. This means my parser receives `1 + a ( 12 )` as input. But I can generate `1 + a ( 12 )` as either of the following:
  - ```
      1 + a(12) \\Arithmetic with the result of a function call
    ```
  - ```
      1 + a \\Constant plus a variable
      (12) \\Constant wrapped in brackets: a valid mathematical expression
    ```
As a result, my grammar in `cfg-v3.txt` is ambiguous which means I won't be able to correctly parse it.

### SOLUTION: Working on it
lol

***