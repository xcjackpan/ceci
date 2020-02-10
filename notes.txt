# problems i face and things i learn along the way

## Order of operations
The terminals that are "deeper" down a parse tree are evaluated first. By having higher-precedence operations
be derived from more rules, we can naturally enforce order of operations.

eg. In `expr -> expr +|- factor`, `factor -> factor *|/ term`, any node representing multiplication or 
division are further down the tree and so are evaluated first.

## Top-down parsers and left/right-recursiveness
A top-down parser (eg. the one I'm building) will immediately recurse itself to death when trying to 
parse a left-recursive grammar. You can see this left-recursive grammar in cfg-v1.txt

But if I use a right-recursive grammar, then everything becomes right-associative. In concrete
terms, `3 - 6 + 8` gets parsed as `3 - (6 + 8)`.

Two solutions: Factor my left-recursive grammar or switch to using a bottom-up parser. :/