from dataclasses import dataclass, field

from src.domain.elements import DocumentElement


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
    """Represents a chapter or section of a book."""

    title: str = ""

    elements: list[DocumentElement] = field(
        default_factory=list
    )

    children: list["Chapter"] = field(
        default_factory=list
    )


@dataclass(slots=True)
class Book:
    """Represents a parsed FB2 book."""

    title: str = ""

    author: Author = field(
        default_factory=Author
    )

    language: str = ""

    resources: dict[str, bytes] = field(
        default_factory=dict
    )

    chapters: list[Chapter] = field(
        default_factory=list
    )