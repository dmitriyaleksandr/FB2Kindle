from pathlib import Path

from ebooklib import epub

from src.domain.book import Book


class EPUBBuilder:
    """Builds EPUB files from Book objects."""

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
            book.title
        )

        epub_book.set_language(
            book.language
        )

        if book.author.full_name:
            epub_book.add_author(
                book.author.full_name
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