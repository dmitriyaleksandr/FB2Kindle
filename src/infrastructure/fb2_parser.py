from pathlib import Path
import xml.etree.ElementTree as ET

from src.domain.book import Author, Book, Chapter
from src.domain.elements import (
    Epigraph,
    Image,
    Paragraph,
    Poem,
    Quote,
    Subtitle,
)


class FB2Parser:
    """Parses FB2 files into domain models."""

    FB2_NS = {
        "fb": "http://www.gribuser.ru/xml/fictionbook/2.0",
        "l": "http://www.w3.org/1999/xlink",
    }

    def parse(self, file_path: Path) -> Book:
        tree = ET.parse(file_path)
        root = tree.getroot()

        return Book(
            title=self._parse_title(root),
            author=self._parse_author(root),
            language=self._parse_language(root),
            chapters=self._parse_chapters(root),
        )

    def _parse_title(self, root: ET.Element) -> str:
        element = root.find(
            "fb:description/fb:title-info/fb:book-title",
            self.FB2_NS,
        )

        return self._get_text(element)

    def _parse_author(self, root: ET.Element) -> Author:
        author = root.find(
            "fb:description/fb:title-info/fb:author",
            self.FB2_NS,
        )

        if author is None:
            return Author()

        return Author(
            first_name=self._get_child_text(
                author,
                "fb:first-name",
            ),
            middle_name=self._get_child_text(
                author,
                "fb:middle-name",
            ),
            last_name=self._get_child_text(
                author,
                "fb:last-name",
            ),
        )

    def _parse_language(self, root: ET.Element) -> str:
        element = root.find(
            "fb:description/fb:title-info/fb:lang",
            self.FB2_NS,
        )

        return self._get_text(element)

    def _parse_chapters(
        self,
        root: ET.Element,
    ) -> list[Chapter]:

        body = root.find(
            "fb:body",
            self.FB2_NS,
        )

        if body is None:
            return []

        return [
            self._parse_section(section)
            for section in body.findall(
                "fb:section",
                self.FB2_NS,
            )
        ]

    def _parse_section(
        self,
        section: ET.Element,
    ) -> Chapter:

        chapter = Chapter(
            title=self._parse_section_title(section)
        )

        for element in section:

            tag = self._remove_namespace(
                element.tag
            )

            if tag == "section":
                chapter.children.append(
                    self._parse_section(element)
                )

            else:
                document_element = (
                    self._parse_document_element(
                        element
                    )
                )

                if document_element:
                    chapter.elements.append(
                        document_element
                    )

        return chapter

    def _parse_document_element(
        self,
        element: ET.Element,
    ):

        tag = self._remove_namespace(
            element.tag
        )

        if tag == "p":
            text = self._get_text(element)

            if text:
                return Paragraph(text)

        if tag == "subtitle":
            text = self._get_text(element)

            if text:
                return Subtitle(text)

        if tag == "epigraph":
            text = self._collect_text(element)

            if text:
                return Epigraph(text)

        if tag == "poem":
            text = self._collect_text(element)

            if text:
                return Poem(text)

        if tag == "cite":
            text = self._collect_text(element)

            if text:
                return Quote(text)

        if tag == "image":
            image_id = element.attrib.get(
                "{http://www.w3.org/1999/xlink}href",
                "",
            )

            if image_id.startswith("#"):
                image_id = image_id[1:]

            if image_id:
                return Image(image_id)

        return None

    def _parse_section_title(
        self,
        section: ET.Element,
    ) -> str:

        title = section.find(
            "fb:title/fb:p",
            self.FB2_NS,
        )

        return self._get_text(title)

    def _collect_text(
        self,
        element: ET.Element,
    ) -> str:

        texts = []

        for child in element.iter():

            if child.text:
                text = child.text.strip()

                if text:
                    texts.append(text)

        return "\n".join(texts)

    def _get_child_text(
        self,
        parent: ET.Element,
        path: str,
    ) -> str:

        element = parent.find(
            path,
            self.FB2_NS,
        )

        return self._get_text(element)

    def _get_text(
        self,
        element: ET.Element | None,
    ) -> str:

        if element is None or element.text is None:
            return ""

        return element.text.strip()

    def _remove_namespace(
        self,
        tag: str,
    ) -> str:

        return tag.split("}")[-1]