"""English pluralization utilities.

Exports:
    pluralize(word: str, count: int = 2) -> str
    singularize(word: str) -> str
    is_plural(word: str) -> bool
"""

from .core import is_plural, pluralize, singularize

__all__ = ["pluralize", "singularize", "is_plural"]
