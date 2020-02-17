These are some notes I'm keeping for stuff I learn along the way.

(This is mostly a learning exercise/for fun so pardon my use of an interpreted language to build
another interpreted language.)

## Order of operations
The terminals that are "deeper" down a parse tree are evaluated first. By having higher-precedence operations
be derived from more rules, our grammar can naturally the mathematical order of operations.

eg. In `expr -> expr +|- factor`, `factor -> factor *|/ term`, any node representing multiplication or 
division are further down the tree and so are evaluated first.

## Top-down parsers and left/right-recursiveness
*Note: A left-recursive grammar is one with rules like `A -> AB`, note how the recursive term `A` occurs on the left of the RHS. A right-recursive grammar is one with rules like `A -> BA`.*

A top-down parser (eg. the one I'm building) will recurses itself to death when trying to 
parse a left-recursive grammar. That's because with a production like `A -> AB`, we'd try to parse the `A` first, which means we'd just use the rule `A -> AB` again. Ideally, we'd want a right-recursive grammar with rules like `A -> BA` so that we would parse `B` using some other rule. You can see this left-recursive grammar in `cfg-v1.txt`. 

But if I use a right-recursive grammar, then everything becomes right-associative. For example, `3 - 6 + 8` gets parsed as `3 - (6 + 8)`. This happens because with rules like `expr -> factor PLUS expr`, the result of parsing the `expr` on the right-hand-side
would be "deeper" down the parse tree than the result of parsing `factor`. This means the `expr` gets evaluated first, resulting
in right-associativity. 

Two possible solutions: Factor my left-recursive grammar or switch to using a bottom-up parser.

## Factoring grammars
My solution to the above problem was to factor my grammar so that it is no longer left-recursive. Compare 
`cfg-v1.txt` with `cfg-v2.txt`.

eg. Replace every derivation `A -> AB` with `A -> Ba, a -> Ba`

The downside of this is that my parse tree gets much larger, but the upside is that it's better trashing
my current top-down parser for a bottom-up one.

## Tests, mathematical expressions, and prefixes
A prefix-free language is one where no word is a prefix of another. For example, `{a, ab}` is **not** 
prefix-free. I designed my grammar to be prefix-free because that makes it easy to parse - once you
see the first token, you know what rule should be used without needing a lookahead.

But in `cfg-v2.txt`, you can see that I didn't account for something: mathematical expressions are a prefix
of boolean tests. You can see how `3 + 5` is a prefix of `3 + 5 < 7`. This means that when our parser sees the 
tokens `3 + 5`, we don't know whether to create a node for `expr` or `test`.