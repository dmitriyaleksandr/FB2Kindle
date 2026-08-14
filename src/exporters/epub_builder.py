from pathlib import Path

from ebooklib import epub

from src.domain.book import Book
from src.exporters.xhtml_renderer import RenderedChapter, XHTMLRenderer


class EPUBBuilder:
    """Builds multi-chapter EPUB files from Book objects."""

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

        chapter_pages = self._build_chapters(
            epub_book,
            book,
        )

        epub_book.toc = tuple(chapter_pages)

        epub_book.add_item(epub.EpubNcx())
        epub_book.add_item(epub.EpubNav())

        epub_book.spine = [
            "nav",
            *chapter_pages,
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
        epub_book.set_title(book.title)
        epub_book.set_language(book.language or "en")

        if book.author.full_name:
            epub_book.add_author(book.author.full_name)

    def _build_chapters(
        self,
        epub_book: epub.EpubBook,
        book: Book,
    ) -> list[epub.EpubHtml]:
        language = book.language or "en"
        chapter_pages = []

        for chapter in self._renderer.render_chapters(book):
            page = self._create_chapter_page(
                chapter,
                language,
            )

            epub_book.add_item(page)
            chapter_pages.append(page)

        return chapter_pages

    def _create_chapter_page(
        self,
        chapter: RenderedChapter,
        language: str,
    ) -> epub.EpubHtml:
        page = epub.EpubHtml(
            title=chapter.title,
            file_name=chapter.file_name,
            lang=language,
        )

        page.content = chapter.content

        return page

    def _write(
        self,
        epub_book: epub.EpubBook,
        output_path: str | Path,
    ) -> None:
        epub.write_epub(
            str(output_path),
            epub_book,
        )