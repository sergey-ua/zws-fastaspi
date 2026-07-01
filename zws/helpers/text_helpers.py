"""Text-related helper functions.

Reusable utilities for working with strings. Currently provides a helper for
counting the number of words in a given string.
"""


def count_words(text: str) -> int:
    """Count the number of words in a given string.

    Words are sequences of non-whitespace characters separated by any
    whitespace (spaces, tabs, newlines). Leading, trailing, and consecutive
    whitespace characters are ignored.

    Args:
        text: The input string to count words in.

    Returns:
        The number of words in ``text``. Returns ``0`` for an empty or
        whitespace-only string.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> count_words("hello world")
        2
        >>> count_words("  the   quick brown fox  ")
        4
        >>> count_words("")
        0
        >>> count_words("   ")
        0
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    return len(text.split())
