# pluralize_py

English pluralisation for Python, with the irregular set included.

```python
from pluralize_py import pluralize, singularize, is_plural

pluralize("cat")        # 'cats'
pluralize("child")      # 'children'
pluralize("cat", 1)     # 'cat'
pluralize("sheep")      # 'sheep'

singularize("children") # 'child'
singularize("cities")   # 'city'

is_plural("cats")       # True
is_plural("cat")        # False
```

## Why this exists

Most pluralisation helpers either ship a full inflection engine (and the
dependency tree that comes with it) or handle only the regular `-s` case.  This
library sits in the middle: it knows the common irregular nouns, the
uncountable nouns, and the handful of regular rules that cover everyday
English, and nothing else.  The trade-off is deliberate — no external
dependencies, no locale data, no attempt to be a complete grammar.  If you need
full coverage, reach for a larger library; if you need `child` -> `children`
and `box` -> `boxes` without pulling in a parser, this is enough.

## API

- `pluralize(word, count=2)` — returns the plural form of `word`.  When
  `count == 1` the singular form is returned.  Raises `ValueError` for an
  empty word or a count below 1.
- `singularize(word)` — returns the singular form of `word`, or the word
  unchanged if it is already singular or uncountable.
- `is_plural(word)` — returns `True` if the word looks like a plural noun.
  Uncountable nouns return `False`, since they are neither singular nor plural.

## The awkward edge

`singularize` cannot always undo `pluralize`.  Words ending in `-ves` are the
clearest case: `pluralize("leaf")` gives `leaves`, but `singularize("leaves")`
gives `leaf` only because `-ives` is special-cased; `pluralize("wife")` gives
`wives`, and `singularize("wives")` gives `wif`, which is not a word.  The
library does not guess between the `-f` and `-fe` sources, because there is no
reliable way to do so without a dictionary.  The README states this limitation
rather than pretending the round trip is lossless.
