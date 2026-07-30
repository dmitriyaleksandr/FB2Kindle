from pathlib import Path

from ebooklib import epub

from src.domain.book import Book
from src.exporters.xhtml_renderer import XHTMLRenderer


class EPUBBuilder:
    """Builds EPUB files from Book objects."""

    def __init__(self) -> None:

        self._renderer = XHTMLRenderer()

    def build(
        self,
        book: Book,
        output_path: str | Path,
    ) -> None:

        epub_book = epub.EpubBook()

        self._build_metadata(
            epub_book,
            book,
        )

        page = self._renderer.render_book(
            book,
        )

        epub_book.add_item(
            page,
        )

        epub_book.toc = (
            page,
        )

        epub_book.add_item(
            epub.EpubNcx(),
        )

        epub_book.add_item(
            epub.EpubNav(),
        )

        epub_book.spine = [
            "nav",
            page,
        ]

        self._write(
            epub_book,
            output_path,
        )

    def _build_metadata(
        self,
        epub_book: epub.EpubBook,
        book: Book,
    ) -> None:

        epub_book.set_title(
            book.title,
        )

        epub_book.set_language(
            book.language,
        )

        if book.author.full_name:
            epub_book.add_author(
                book.author.full_name,
            )

    def _write(
        self,
        epub_book: epub.EpubBook,
        output_path: str | Path,
    ) -> None:

        epub.write_epub(
            str(output_path),
            epub_book,
        )