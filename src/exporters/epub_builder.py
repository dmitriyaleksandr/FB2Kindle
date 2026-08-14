from pathlib import Path

from ebooklib import epub

from src.domain.book import Book
from src.exporters.xhtml_renderer import RenderedChapter, XHTMLRenderer


class EPUBBuilder:
    """Builds multi-chapter EPUB files from Book objects."""

    STYLESHEET_PATH = Path(__file__).parent / "assets" / "style.css"
    STYLESHEET_FILE_NAME = "styles/style.css"

    def __init__(self) -> None:

        self._renderer = XHTMLRenderer()

    def build(
        self,
        book: Book,
        output_path: str | Path,
    ) -> None:

        epub_book = epub.EpubBook()

        self._build_metadata(epub_book, book)

        image_paths = self._add_images(epub_book, book)
        stylesheet = self._add_stylesheet(epub_book)
        chapter_pages = self._build_chapters(
            epub_book,
            book,
            image_paths,
            stylesheet,
        )

        epub_book.toc = tuple(chapter_pages)

        epub_book.add_item(epub.EpubNcx())
        epub_book.add_item(epub.EpubNav())

        epub_book.spine = [
            "nav",
            *chapter_pages,
        ]

        self._write(epub_book, output_path)

    def _build_metadata(
        self,
        epub_book: epub.EpubBook,
        book: Book,
    ) -> None:

        epub_book.set_title(book.title)
        epub_book.set_language(book.language or "en")

        if book.author.full_name:
            epub_book.add_author(book.author.full_name)

    def _add_images(
        self,
        epub_book: epub.EpubBook,
        book: Book,
    ) -> dict[str, str]:

        image_paths = {}

        for index, (image_id, content) in enumerate(
            book.resources.items(),
            start=1,
        ):
            image_type = self._get_image_type(content)

            if image_type is None:
                continue

            extension, media_type = image_type
            file_name = f"images/image_{index:03}{extension}"

            epub_book.add_item(
                epub.EpubImage(
                    uid=f"image_{index:03}",
                    file_name=file_name,
                    media_type=media_type,
                    content=content,
                )
            )

            image_paths[image_id] = file_name

        return image_paths

    def _add_stylesheet(
        self,
        epub_book: epub.EpubBook,
    ) -> epub.EpubItem:

        stylesheet = epub.EpubItem(
            uid="stylesheet",
            file_name=self.STYLESHEET_FILE_NAME,
            media_type="text/css",
            content=self.STYLESHEET_PATH.read_bytes(),
        )

        epub_book.add_item(stylesheet)

        return stylesheet

    @staticmethod
    def _get_image_type(
        content: bytes,
    ) -> tuple[str, str] | None:

        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return ".png", "image/png"

        if content.startswith(b"\xff\xd8\xff"):
            return ".jpg", "image/jpeg"

        if content.startswith((b"GIF87a", b"GIF89a")):
            return ".gif", "image/gif"

        if content.startswith(b"BM"):
            return ".bmp", "image/bmp"

        if (
            content.startswith(b"RIFF")
            and content[8:12] == b"WEBP"
        ):
            return ".webp", "image/webp"

        if content.startswith((b"II*\x00", b"MM\x00*")):
            return ".tiff", "image/tiff"

        if b"<svg" in content[:1024].lower():
            return ".svg", "image/svg+xml"

        return None

    def _build_chapters(
        self,
        epub_book: epub.EpubBook,
        book: Book,
        image_paths: dict[str, str],
        stylesheet: epub.EpubItem,
    ) -> list[epub.EpubHtml]:

        language = book.language or "en"
        chapter_pages = []

        for chapter in self._renderer.render_chapters(book, image_paths):
            page = self._create_chapter_page(
                chapter,
                language,
                stylesheet,
            )

            epub_book.add_item(page)
            chapter_pages.append(page)

        return chapter_pages

    def _create_chapter_page(
        self,
        chapter: RenderedChapter,
        language: str,
        stylesheet: epub.EpubItem,
    ) -> epub.EpubHtml:

        page = epub.EpubHtml(
            title=chapter.title,
            file_name=chapter.file_name,
            lang=language,
        )

        page.content = chapter.content
        page.add_item(stylesheet)

        return page

    def _write(
        self,
        epub_book: epub.EpubBook,
        output_path: str | Path,
    ) -> None:

        epub.write_epub(str(output_path), epub_book)
