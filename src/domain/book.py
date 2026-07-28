from dataclasses import dataclass, field


@dataclass(slots=True)
class Author:
    """Represents a book author."""

    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""

    @property
    def full_name(self) -> str:
        return " ".join(
            part
            for part in (
                self.first_name,
                self.middle_name,
                self.last_name,
            )
            if part
        )


@dataclass(slots=True)
class Chapter:
    """Represents a single book chapter."""

    title: str
    content: str


@dataclass(slots=True)
class Book:
    """Represents a parsed FB2 book."""

    title: str = ""
    author: Author = field(default_factory=Author)
    language: str = ""
    cover: bytes | None = None
    chapters: list[Chapter] = field(default_factory=list)