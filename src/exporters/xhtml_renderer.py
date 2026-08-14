from ebooklib import epub

from src.domain.book import Book
from src.domain.book import Chapter
from src.domain.elements import (
    DocumentElement,
    Epigraph,
    Image,
    Paragraph,
    Poem,
    Quote,
    Subtitle,
)


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
            return self._render_paragraph(
                element,
            )

        if isinstance(
            element,
            Subtitle,
        ):
            return self._render_subtitle(
                element,
            )

        if isinstance(
            element,
            Epigraph,
        ):
            return self._render_epigraph(
                element,
            )

        if isinstance(
            element,
            Quote,
        ):
            return self._render_quote(
                element,
            )

        if isinstance(
            element,
            Poem,
        ):
            return self._render_poem(
                element,
            )

        if isinstance(
            element,
            Image,
        ):
            return self._render_image(
                element,
            )

        return []

    def _render_paragraph(
        self,
        paragraph: Paragraph,
    ) -> list[str]:

        return [
            f"<p>{paragraph.text}</p>",
        ]

    def _render_subtitle(
        self,
        subtitle: Subtitle,
    ) -> list[str]:

        return [
            f"<h3>{subtitle.text}</h3>",
        ]

    def _render_epigraph(
        self,
        epigraph: Epigraph,
    ) -> list[str]:

        return [
            "<blockquote>",
            f"<p>{epigraph.text}</p>",
            "</blockquote>",
        ]

    def _render_quote(
        self,
        quote: Quote,
    ) -> list[str]:

        return [
            "<blockquote>",
            f"<p>{quote.text}</p>",
            "</blockquote>",
        ]

    def _render_poem(
        self,
        poem: Poem,
    ) -> list[str]:

        html = [
            "<div class=\"poem\">",
        ]

        for line in poem.text.split("\n"):
            html.append(
                f"{line}<br/>"
            )

        html.append(
            "</div>"
        )

        return html

    def _render_image(
        self,
        image: Image,
    ) -> list[str]:

        return []