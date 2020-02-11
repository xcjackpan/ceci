These are some notes I'm keeping for stuff I learn along the way.

(This is mostly a learning exercise/for fun so pardon my use of an interpreted language to build
and interpreted language.)

## Order of operations
The terminals that are "deeper" down a parse tree are evaluated first. By having higher-precedence operations
be derived from more rules, our grammar naturally enforces the order of operations.

eg. In `expr -> expr +|- factor`, `factor -> factor *|/ term`, any node representing multiplication or 
division are further down the tree and so are evaluated first.

## Top-down parsers and left/right-recursiveness
A top-down parser (eg. the one I'm building) will immediately recurse itself to death when trying to 
parse a left-recursive grammar. You can see this left-recursive grammar in `cfg-v1.txt`

But if I use a right-recursive grammar, then everything becomes right-associative. In concrete
terms, `3 - 6 + 8` gets parsed as `3 - (6 + 8)`.

Two solutions: Factor my left-recursive grammar or switch to using a bottom-up parser. Oof.

## Factoring grammars
My solution to the above problem was to factor my grammar so that it is no longer left-recursive. Compare `cfg-v1.txt`
with `cfg-v2.txt`.

eg. Replace every derivation `A -> AB` with `A -> Ba, a -> Ba`

The downside of this is that my parse tree gets much larger, but the upside is that it's better trashing
my current top-down parser for a bottom-up one.