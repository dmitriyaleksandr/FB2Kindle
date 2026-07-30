from ebooklib import epub

from src.domain.book import Book
from src.domain.book import Chapter
from src.domain.elements import DocumentElement
from src.domain.elements import Paragraph


class XHTMLRenderer:
    """Renders Book objects into XHTML documents."""

    def render_book(
        self,
        book: Book,
    ) -> epub.EpubHtml:

        page = epub.EpubHtml(
            title=book.title,
            file_name="index.xhtml",
            lang=book.language,
        )

        html = [
            "<html>",
            "<body>",
            f"<h1>{book.title}</h1>",
        ]

        for chapter in book.chapters:
            html.extend(
                self._render_chapter(
                    chapter,
                )
            )

        html.extend(
            [
                "</body>",
                "</html>",
            ]
        )

        page.content = "\n".join(html)

        return page

    def _render_chapter(
        self,
        chapter: Chapter,
    ) -> list[str]:

        html = []

        if chapter.title:
            html.append(
                f"<h2>{chapter.title}</h2>"
            )

        for element in chapter.elements:
            html.extend(
                self._render_element(
                    element,
                )
            )

        for child in chapter.children:
            html.extend(
                self._render_chapter(
                    child,
                )
            )

        return html

    def _render_element(
        self,
        element: DocumentElement,
    ) -> list[str]:

        if isinstance(
            element,
            Paragraph,
        ):
            return [
                f"<p>{element.text}</p>"
            ]

        return []