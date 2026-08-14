from collections.abc import Mapping
from dataclasses import dataclass
from html import escape

from src.domain.book import Book, Chapter
from src.domain.elements import (
    DocumentElement,
    Epigraph,
    Image,
    Paragraph,
    Poem,
    Quote,
    Subtitle,
)


@dataclass(frozen=True, slots=True)
class RenderedChapter:
    title: str
    file_name: str
    content: str


class XHTMLRenderer:
    """Renders Book chapters into EPUB-independent XHTML fragments."""

    def render_chapters(
        self,
        book: Book,
        image_paths: Mapping[str, str] | None = None,
    ) -> list[RenderedChapter]:
        rendered_chapters: list[RenderedChapter] = []
        image_paths = image_paths or {}

        for chapter in book.chapters:
            self._render_chapter_tree(
                chapter,
                rendered_chapters,
                image_paths,
            )

        if not rendered_chapters:
            rendered_chapters.append(
                RenderedChapter(
                    title=book.title or "Untitled",
                    file_name="chapter_001.xhtml",
                    content=self._render_empty_book(book),
                )
            )

        return rendered_chapters

    def _render_chapter_tree(
        self,
        chapter: Chapter,
        rendered_chapters: list[RenderedChapter],
        image_paths: Mapping[str, str],
    ) -> None:
        chapter_number = len(rendered_chapters) + 1
        title = chapter.title or f"Chapter {chapter_number}"

        rendered_chapters.append(
            RenderedChapter(
                title=title,
                file_name=f"chapter_{chapter_number:03}.xhtml",
                content=self._render_chapter(chapter, image_paths) or "<p></p>",
            )
        )

        for child in chapter.children:
            self._render_chapter_tree(
                child,
                rendered_chapters,
                image_paths,
            )

    def _render_empty_book(
        self,
        book: Book,
    ) -> str:
        if not book.title:
            return ""

        return f"<h1>{escape(book.title)}</h1>"

    def _render_chapter(
        self,
        chapter: Chapter,
        image_paths: Mapping[str, str],
    ) -> str:
        html: list[str] = []

        if chapter.title:
            html.append(f"<h1>{escape(chapter.title)}</h1>")

        for element in chapter.elements:
            html.extend(self._render_element(element, image_paths))

        return "\n".join(html)

    def _render_element(
        self,
        element: DocumentElement,
        image_paths: Mapping[str, str],
    ) -> list[str]:
        if isinstance(element, Paragraph):
            return self._render_paragraph(element)

        if isinstance(element, Subtitle):
            return self._render_subtitle(element)

        if isinstance(element, Epigraph):
            return self._render_epigraph(element)

        if isinstance(element, Quote):
            return self._render_quote(element)

        if isinstance(element, Poem):
            return self._render_poem(element)

        if isinstance(element, Image):
            return self._render_image(element, image_paths)

        return []

    def _render_paragraph(
        self,
        paragraph: Paragraph,
    ) -> list[str]:
        return [f"<p>{escape(paragraph.text)}</p>"]

    def _render_subtitle(
        self,
        subtitle: Subtitle,
    ) -> list[str]:
        return [f"<h2>{escape(subtitle.text)}</h2>"]

    def _render_epigraph(
        self,
        epigraph: Epigraph,
    ) -> list[str]:
        return self._render_blockquote(epigraph.text)

    def _render_quote(
        self,
        quote: Quote,
    ) -> list[str]:
        return self._render_blockquote(quote.text)

    def _render_blockquote(
        self,
        text: str,
    ) -> list[str]:
        return [
            "<blockquote>",
            *(
                f"<p>{escape(paragraph)}</p>"
                for paragraph in text.split("\n")
                if paragraph
            ),
            "</blockquote>",
        ]

    def _render_poem(
        self,
        poem: Poem,
    ) -> list[str]:
        lines = ["<div class=\"poem\">"]

        for line in poem.text.split("\n"):
            lines.append(f"{escape(line)}<br />")

        lines.append("</div>")

        return lines

    def _render_image(
        self,
        image: Image,
        image_paths: Mapping[str, str],
    ) -> list[str]:
        source = image_paths.get(image.image_id)

        if source is None:
            return []

        return [
            '<figure class="image">',
            f'<img src="{escape(source, quote=True)}" alt="" />',
            "</figure>",
        ]