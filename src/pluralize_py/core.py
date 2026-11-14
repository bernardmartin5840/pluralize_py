"""Core pluralization logic.

The module keeps three tables:

* ``_IRREGULAR`` maps a singular form to its plural.  The reverse mapping is
  built at import time so the two directions cannot drift apart.
* ``_UNCOUNTABLE`` is a set of nouns that do not change number.
* ``_RULES`` is an ordered list of (compiled regex, replacement) pairs used for
  the regular cases.  Order matters: the first rule that matches wins, so the
  more specific patterns are listed before the general ones.

A deliberate simplification: the library does not attempt to inflect numbers
or determiners, and it does not handle words that are plural-only ("scissors",
"trousers").  Those are documented in the README as known limitations.
"""

from __future__ import annotations

import re
from typing import Dict, List, Pattern, Tuple

# Irregular nouns: singular -> plural.
_IRREGULAR: Dict[str, str] = {
    "child": "children",
    "foot": "feet",
    "goose": "geese",
    "man": "men",
    "mouse": "mice",
    "person": "people",
    "tooth": "teeth",
    "woman": "women",
    "ox": "oxen",
}

# Reverse mapping, built once so the two directions stay consistent.
_IRREGULAR_REVERSE: Dict[str, str] = {v: k for k, v in _IRREGULAR.items()}

# Nouns that are the same in both numbers.
_UNCOUNTABLE = {
    "equipment",
    "information",
    "rice",
    "money",
    "species",
    "series",
    "fish",
    "sheep",
    "deer",
}

# Regular rules, applied in order; the first match wins.
_RULES: List[Tuple[Pattern[str], str]] = [
    (re.compile(r"(s|ss|sh|ch|x|z)$", re.IGNORECASE), r"\1es"),
    (re.compile(r"([^aeiou])y$", re.IGNORECASE), r"\1ies"),
    (re.compile(r"(f|fe)$", re.IGNORECASE), "ves"),
    (re.compile(r"$"), "s"),
]


def _match_case(source: str, target: str) -> str:
    """Return *target* with the capitalisation pattern of *source*.

    Only the first character is considered.  That covers the cases this
    library cares about ("Cat" -> "Cats", "CAT" -> "CATS") without
    pretending to handle mixed-case input such as "cAt".
    """
    if not source or not target:
        return target
    if source.isupper():
        return target.upper()
    if source[0].isupper():
        return target[0].upper() + target[1:]
    return target


def _apply_rules(word: str) -> str:
    """Apply the first matching regular rule to *word*."""
    for pattern, replacement in _RULES:
        if pattern.search(word):
            return pattern.sub(replacement, word)
    # The final rule always matches, so this is unreachable in practice.
    return word + "s"


def pluralize(word: str, count: int = 2) -> str:
    """Return the plural form of *word*.

    ``count`` is the number the word refers to.  When ``count == 1`` the
    singular form is returned, which matches the way the word is actually
    used in a sentence.  Every other value (including zero and negatives)
    yields the plural.

    ``ValueError`` is raised for a non-positive ``count`` because a count of
    zero or less has no sensible grammatical number.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    if count < 1:
        raise ValueError("count must be at least 1")

    if count == 1:
        return word

    lower = word.lower()
    if lower in _UNCOUNTABLE:
        return word
    if lower in _IRREGULAR:
        return _match_case(word, _IRREGULAR[lower])

    return _apply_rules(word)


def singularize(word: str) -> str:
    """Return the singular form of *word*.

    The reverse of :func:`pluralize` for the irregular and uncountable sets,
    and a best-effort regular reverse otherwise.  Words that are already
    singular are returned unchanged.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")

    lower = word.lower()
    if lower in _UNCOUNTABLE or lower in _IRREGULAR:
        return word
    if lower in _IRREGULAR_REVERSE:
        return _match_case(word, _IRREGULAR_REVERSE[lower])

    if lower.endswith("ies") and len(lower) > 3:
        return word[:-3] + "y"
    if lower.endswith("ves"):
        # The regular plural of a word ending in -f or -fe is -ves, but the
        # singular cannot be recovered reliably ("leaves" -> "leaf" or
        # "leafe"?).  Only the common -fe case is reversed here.
        if lower.endswith("ives"):
            return word[:-3] + "fe"
        return word[:-3] + "f"
    if lower.endswith("es"):
        return word[:-2]
    if lower.endswith("s") and not lower.endswith("ss"):
        return word[:-1]
    return word


def is_plural(word: str) -> bool:
    """Return ``True`` if *word* looks like a plural noun.

    The check is heuristic: it is the inverse of :func:`singularize` for the
    forms this library knows about.  A word that is already singular returns
    ``False``.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")

    lower = word.lower()
    if lower in _UNCOUNTABLE:
        # Uncountable nouns are neither singular nor plural; the conservative
        # answer is ``False``.
        return False
    if lower in _IRREGULAR_REVERSE:
        return True
    if lower in _IRREGULAR:
        return False

    if lower.endswith("ies") and len(lower) > 3:
        return True
    if lower.endswith("ves"):
        return True
    if lower.endswith("es"):
        return True
    if lower.endswith("s") and not lower.endswith("ss"):
        return True
    return False
