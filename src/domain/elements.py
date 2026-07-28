from dataclasses import dataclass


class DocumentElement:
    """Base class for all document elements."""

    pass


@dataclass(slots=True)
class Paragraph(DocumentElement):
    """Regular paragraph."""

    text: str


@dataclass(slots=True)
class Subtitle(DocumentElement):
    """Subtitle inside a chapter."""

    text: str


@dataclass(slots=True)
class Epigraph(DocumentElement):
    """Book epigraph."""

    text: str


@dataclass(slots=True)
class Quote(DocumentElement):
    """Quoted text."""

    text: str


@dataclass(slots=True)
class Poem(DocumentElement):
    """Poem block."""

    text: str


@dataclass(slots=True)
class Image(DocumentElement):
    """Embedded image reference."""

    image_id: str