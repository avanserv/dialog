import re
import textwrap
from collections.abc import Sequence


__all__ = [
    "list_styles",
    "normalize_indent",
    "resolve_styles",
    "stylize",
]


def normalize_indent(text: str) -> str:
    """Normalize the indentation of a string.

    :param text: The text to normalize.
    :return: The normalized text.
    :rtype: str
    """
    if "\n" in text.strip():
        min_indent = min(len(line) - len(line.lstrip()) for line in text.splitlines()[1:] if line.strip())
        text = " " * min_indent + text
    return textwrap.dedent(text).strip()


def list_styles(text: str) -> list[str]:
    """Extract Rich styles from a text and returns the list of tags in their order of appearance.
    Only lists unique opening tags, closing tags are ignored. Nested tags are supported.
    :param text: The text to list styles from.
    """
    return re.findall(r"\[(?!\/)([\w\.]+(?:\s+[\w\.]+)*)\]", text)


def stylize(value: str, style: str) -> str:
    """Stylize a value to use with Rich markup.
    :param value: The value to stylize.
    :param style: The style to apply.
    :return: The stylized value.
    :rtype: str
    """
    from .console import resolve_styles

    style = resolve_styles(style)
    return f"[{style}]{value}[/{style}]"


def resolve_styles(text: str) -> str:
    """Resolve markup styles from a text, replacing aliased styles by their proper value usable by Rich.
    :param text: The text to resolve styles from.
    """
    from .console import resolve_styles

    def replace_tag(match: re.Match) -> str:
        tag = f"{match.group(1)} {replacement} {match.group(2)}".strip()
        return stylize(match.group(3), tag)

    for style in list_styles(text):
        replacement = resolve_styles(style)
        tag = re.escape(style)
        text = re.sub(rf"\[(.*?)(?:{tag})(.*?)\](.*?)\[\/\1(?:{tag})\2\]", replace_tag, text)

    return text


def join(parts: Sequence[str], last_delimiter: str | None = None) -> str:
    """Join parts, optionally adding a last delimiter between the last two items.
    :param parts: Parts to join.
    :param last_delimiter: The last delimiter to add.
    :return: The joined parts.
    :rtype: str
    """
    if not parts:
        return ""

    if len(parts) == 1:
        return parts[0]

    if last_delimiter is None:
        return ", ".join(parts)

    return ", ".join(parts[:-1]) + f" {last_delimiter} {parts[-1]}"


def join_and(parts: Sequence[str]) -> str:
    """Join parts adding "and" between the two lasts items.
    :param parts: Parts to join.
    :return: The joined parts.
    :rtype: str
    """
    return join(parts, "and")


def join_or(parts: Sequence[str]) -> str:
    """Join parts adding "or" between the two lasts items.
    :param parts: Parts to join.
    :return: The joined parts.
    :rtype: str
    """
    return join(parts, "or")


def join_bullet(parts: Sequence[str]) -> str:
    """Join parts as a bullet list.
    :param parts: Parts to join.
    :return: The joined parts.
    :rtype: str
    """
    bullet = "\n•"
    return "".join([f"{bullet} {part}" for part in parts]).strip()
