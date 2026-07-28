from dataclasses import dataclass, field


@dataclass(slots=True)
class Chapter:
    """Represents a single book chapter."""

    title: str
    content: str


@dataclass(slots=True)
class Book:
    """Represents a parsed FB2 book."""

    title: str = ""
    author: str = ""
    language: str = ""
    cover: bytes | None = None
    chapters: list[Chapter] = field(default_factory=list)